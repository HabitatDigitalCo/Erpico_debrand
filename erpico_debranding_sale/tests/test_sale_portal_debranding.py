# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from unittest.mock import patch

from odoo.tests import HttpCase, TransactionCase, tagged
from odoo.tests.common import new_test_user


@tagged('erpico_debranding', '-at_install', 'post_install')
class TestSalePortalDebranding(HttpCase):

    def _assert_edi_button_hidden(self, model, view_xmlid, path):
        partner = self.env['res.partner'].create({'name': 'Portal EDI Test'})
        order = self.env[model].create({'partner_id': partner.id})
        token = order._portal_ensure_token()
        view = self.env.ref(view_xmlid)
        url = path % order.id
        with patch.object(type(order), '_get_edi_builders', return_value=[object()]):
            view.active = False
            try:
                original = self.url_open(url, params={'access_token': token})
                self.assertEqual(original.status_code, 200)
                self.assertIn('portal_connect_software_modal_btn', original.text)
            finally:
                view.active = True
            response = self.url_open(url, params={'access_token': token})
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('portal_connect_software_modal_btn', response.text)
            self.assertNotIn('portal_connect_software_modal', response.text)

    def test_sale_edi_button_hidden_when_original_would_show(self):
        self._assert_edi_button_hidden(
            'sale.order', 'erpico_debranding_sale.sale_hide_connect_software',
            '/my/orders/%s')

    def test_purchase_edi_button_hidden_when_original_would_show(self):
        self._assert_edi_button_hidden(
            'purchase.order', 'erpico_debranding_sale.purchase_hide_connect_software',
            '/my/purchase/%s')

    def test_portal_orders_require_valid_access(self):
        partner = self.env['res.partner'].create({'name': 'Portal Access Test'})
        for model, path in (
            ('sale.order', '/my/orders/%s'),
            ('purchase.order', '/my/purchase/%s'),
        ):
            order = self.env[model].create({'partner_id': partner.id})
            order._portal_ensure_token()
            for params in ({}, {'access_token': 'invalid-synthetic-token'}):
                response = self.url_open(path % order.id, params=params, allow_redirects=False)
                self.assertIn(response.status_code, (302, 303), (model, params))

    def test_sale_order_portal_hides_connect_software(self):
        partner = self.env['res.partner'].create({'name': 'Portal Test'})
        order = self.env['sale.order'].create({
            'partner_id': partner.id,
        })
        access_token = order._portal_ensure_token()
        self.assertTrue(access_token, "access_token not generated")
        response = self.url_open(
            '/my/orders/%s?access_token=%s' % (order.id, access_token))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Connect with your software!', response.text)
        self.assertNotIn('portal_connect_software_modal', response.text)

    def test_purchase_order_portal_hides_connect_software(self):
        partner = self.env['res.partner'].create({'name': 'Portal Test'})
        order = self.env['purchase.order'].create({
            'partner_id': partner.id,
        })
        access_token = order._portal_ensure_token()
        self.assertTrue(access_token, "access_token not generated")
        response = self.url_open(
            '/my/purchase/%s?access_token=%s' % (order.id, access_token))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Connect with your software!', response.text)
        self.assertNotIn('portal_connect_software_modal', response.text)


@tagged('erpico_debranding')
class TestSalePortalOverride(TransactionCase):

    def test_sale_override_templates_registered(self):
        """Los overrides QWeb existen en el modelo de vistas."""
        for xmlid in (
            'erpico_debranding_sale.sale_hide_connect_software',
            'erpico_debranding_sale.purchase_hide_connect_software',
            'erpico_debranding_sale.purchase_order_hide_connect_software',
            'erpico_debranding_sale.purchase_quotation_hide_connect_software',
        ):
            self.assertTrue(self.env.ref(xmlid), xmlid)

    def test_purchase_reports_hide_edi_link_when_original_would_show(self):
        portal_user = new_test_user(
            self.env, login='edi-portal@example.test', groups='base.group_portal',
            context={'no_reset_password': True},
        )
        order = self.env['purchase.order'].create({'partner_id': portal_user.partner_id.id})
        reports = (
            ('purchase.action_report_purchase_order',
             'erpico_debranding_sale.purchase_order_hide_connect_software'),
            ('purchase.report_purchase_quotation',
             'erpico_debranding_sale.purchase_quotation_hide_connect_software'),
        )
        renderer = self.env['ir.actions.report']
        with patch.object(type(order), '_get_edi_builders', return_value=[object()]):
            for report_xmlid, view_xmlid in reports:
                view = self.env.ref(view_xmlid)
                view.active = False
                try:
                    original, _ = renderer._render_qweb_html(report_xmlid, order.ids)
                    self.assertIn(b'#portal_connect_software_modal', original)
                finally:
                    view.active = True
                rendered, _ = renderer._render_qweb_html(report_xmlid, order.ids)
                self.assertNotIn(b'#portal_connect_software_modal', rendered)
