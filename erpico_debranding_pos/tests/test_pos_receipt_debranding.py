# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from pathlib import Path

from odoo.tests import TransactionCase, tagged


@tagged('erpico_debranding')
class TestPosReceiptDebranding(TransactionCase):

    def test_override_registered_in_assets(self):
        """El override del recibo está en el bundle de assets del POS."""
        paths = self.env['ir.asset']._get_asset_paths(
            'point_of_sale.assets_prod', {})
        self.assertTrue(
            any(
                p[0].endswith(
                    'erpico_debranding_pos/static/src/override/order_receipt.xml')
                for p in paths
            ),
            "order_receipt.xml not in point_of_sale.assets_prod",
        )

    def test_override_targets_order_receipt(self):
        """El override apunta a OrderReceipt y debranda el footer."""
        path = (
            Path(__file__).resolve().parents[1]
            / 'static' / 'src' / 'override' / 'order_receipt.xml'
        )
        xml = path.read_text(encoding='utf-8')
        self.assertIn('t-inherit="point_of_sale.OrderReceipt"', xml)
        self.assertIn('Powered by <b>ERPICO</b>', xml)
        self.assertNotIn('Powered by Odoo', xml)

    def test_customer_display_override_registered_in_separate_bundle(self):
        paths = self.env['ir.asset']._get_asset_paths(
            'point_of_sale.customer_display_assets', {})
        self.assertTrue(any(
            item[0].endswith('erpico_debranding_pos/static/src/override/customer_display.xml')
            for item in paths
        ))

    def test_receipt_override_registered_in_dark_bundle(self):
        paths = self.env['ir.asset']._get_asset_paths(
            'point_of_sale.assets_prod_dark', {})
        self.assertTrue(any(
            item[0].endswith('erpico_debranding_pos/static/src/override/order_receipt.xml')
            for item in paths
        ))
