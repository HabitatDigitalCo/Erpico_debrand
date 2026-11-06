/* © 2026 Habitat Digital */
/* License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html). */

import { Component, xml } from "@odoo/owl";
import { expect, test } from "@odoo/hoot";
import { queryAll, queryOne } from "@odoo/hoot-dom";
import { mountWithCleanup } from "@web/../tests/web_test_helpers";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { definePosModels } from "@point_of_sale/../tests/unit/data/generate_model_definitions";
import { getFilledOrder, setupPosEnv } from "@point_of_sale/../tests/unit/utils";

definePosModels();

for (const scenario of [
    { name: "sale", basic: false, refund: false },
    { name: "refund", basic: false, refund: true },
    { name: "basic receipt", basic: true, refund: false },
]) {
    test.tags("erpico_debranding_pos");
    test(`ERPICO receipt renders for ${scenario.name}`, async () => {
        const store = await setupPosEnv();
        const order = await getFilledOrder(store, {}, false, scenario.refund);
        await mountWithCleanup(OrderReceipt, {
            props: { order, basic_receipt: scenario.basic },
        });
        expect(queryAll(".footer-powered-by")).toHaveLength(1);
        expect(queryOne(".footer-powered-by").textContent.replace(/\s+/g, " ").trim())
            .toBe("Powered by ERPICO");
        expect(queryAll(".pos-receipt .orderline").length > 0).toBe(true);
        expect(queryAll(".pos-receipt .receipt-total")).toHaveLength(scenario.basic ? 0 : 1);
    });
}

class EmptyComponent extends Component {
    static template = xml`<div/>`;
    static props = ["*"];
}

class CustomerDisplayProbe extends Component {
    static template = "point_of_sale.CustomerDisplay";
    static props = { order: Object };
    static components = {
        OdooLogo: EmptyComponent,
        MainComponentsContainer: EmptyComponent,
        TagsList: EmptyComponent,
    };

    setup() {
        this.order = this.props.order;
        this.session = { has_bg_img: false, company_id: 1 };
        this.pos = { config: { id: 1 } };
    }

    getInternalNotes() {
        return [];
    }
}

for (const order of [
    { lines: [], finalized: false },
    { lines: [], finalized: true },
    {
        lines: [{ productId: 1, productName: "Product", price: "$20", qty: 1, unitPrice: "$20" }],
        finalized: false,
        amount: "$20",
    },
]) {
    test.tags("erpico_debranding_pos");
    test(`ERPICO customer display renders with ${order.lines.length} lines and finalized=${order.finalized}`, async () => {
        await mountWithCleanup(CustomerDisplayProbe, {
            props: { order },
        });
        const display = queryOne(".o_customer_display");
        expect(queryAll(".o_customer_display b")).toHaveLength(2);
        expect(display.textContent.includes("Odoo")).toBe(false);
        expect(display.textContent.match(/ERPICO/g)).toHaveLength(2);
        if (order.lines.length) {
            expect(display.textContent.includes("$20")).toBe(true);
        }
    });
}
