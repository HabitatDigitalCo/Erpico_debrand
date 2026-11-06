# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import base64

from lxml import etree

from odoo import tools
from odoo.addons.erpico_debranding import _rebrand_bot_partner
from odoo.addons.erpico_debranding.patches import legacy_emails
from odoo.addons.erpico_debranding.patches.legacy_emails import (
    LEGACY_EMAIL_XMLIDS,
)
from odoo.tests import HttpCase, TransactionCase, tagged
from odoo.tools.safe_eval import safe_eval


@tagged('erpico_debranding')
class TestLegacyEmails(TransactionCase):

    def test_legacy_bodies_rebranded(self):
        for xmlid in LEGACY_EMAIL_XMLIDS:
            body = str(self.env.ref(xmlid).body_html or '')
            self.assertNotIn('Odoo', body, xmlid)
            self.assertNotIn('odoo.com', body, xmlid)
        # el template de set-password lleva marca ERPICO tras el parche
        set_password_body = str(
            self.env.ref('auth_signup.set_password_email').body_html or '')
        self.assertIn('ERPICO', set_password_body)

    def test_bot_partner_renamed(self):
        self.assertEqual(self.env.ref('base.partner_root').name, 'ERPICO Assistant')

    def test_invitation_subject_rebranded(self):
        template = self.env.ref('auth_signup.set_password_email').with_context(lang='en_US')
        subject = template.subject
        self.assertIn('ERPICO', subject)
        self.assertNotIn('Odoo', subject)
        rendered = template._render_field('subject', [self.env.user.id])[self.env.user.id]
        self.assertIn('ERPICO', rendered)
        self.assertNotIn('Odoo', rendered)
        body = template._render_field('body_html', [self.env.user.id])[self.env.user.id]
        self.assertIn('ERPICO', str(body))
        self.assertIn('href=', str(body))
        self.assertNotIn('odoo.com', str(body))

    def test_custom_template_and_other_contact_are_preserved(self):
        template = self.env.ref('auth_signup.set_password_email').with_context(lang='en_US')
        template.write({
            'subject': 'Custom Odoo invitation',
            'body_html': '<p>Welcome to Odoo - custom content</p>',
        })
        contact = self.env['res.partner'].create({'name': 'OdooBot'})
        legacy_emails.patch_legacy_emails(self.env)
        self.assertEqual(template.subject, 'Custom Odoo invitation')
        self.assertIn('Welcome to Odoo - custom content', str(template.body_html))
        self.assertEqual(contact.name, 'OdooBot')

    def test_custom_bot_identity_is_preserved(self):
        bot = self.env.ref('base.partner_root')
        with tools.file_open('base/static/img/res_company_logo.png', 'rb') as image:
            bot.write({'name': 'Custom Assistant', 'image_1920': base64.b64encode(image.read())})
        before = bot.image_1920
        _rebrand_bot_partner(self.env)
        self.assertEqual(bot.name, 'Custom Assistant')
        self.assertEqual(bot.image_1920, before)

    def test_custom_bot_image_is_preserved_with_stock_name(self):
        bot = self.env.ref('base.partner_root')
        with tools.file_open('base/static/img/res_company_logo.png', 'rb') as image:
            bot.write({'name': 'OdooBot', 'image_1920': base64.b64encode(image.read())})
        before = bot.image_1920
        _rebrand_bot_partner(self.env)
        self.assertEqual(bot.name, 'ERPICO Assistant')
        self.assertEqual(bot.image_1920, before)


@tagged('erpico_debranding')
class TestEnterpriseHidden(TransactionCase):

    def test_module_hidden_only_in_catalog_action(self):
        module = self.env['ir.module.module'].create({
            'name': 'test_enterprise_hidden',
            'state': 'uninstalled',
            'to_buy': True,
        })
        modules = self.env['ir.module.module']
        self.assertIn(module, modules.search([('id', '=', module.id)]))
        self.assertEqual(modules.search_count([('id', '=', module.id)]), 1)
        action = self.env.ref('base.open_module_tree')._get_action_dict()
        self.assertNotIn(module, modules.search(safe_eval(action['domain'])))

    def test_provider_hidden_only_in_catalog_action(self):
        module = self.env['ir.module.module'].create({
            'name': 'test_enterprise_module',
            'state': 'uninstalled',
            'to_buy': True,
        })
        provider = self.env['payment.provider'].create({
            'name': 'Test Enterprise Provider',
            'code': 'none',
            'module_id': module.id,
            'state': 'enabled',
            'is_published': True,
        })
        providers = self.env['payment.provider']
        self.assertIn(provider, providers.search([('id', '=', provider.id)]))
        self.assertEqual(providers.search_count([('id', '=', provider.id)]), 1)
        action = self.env.ref('payment.action_payment_provider')._get_action_dict()
        self.assertNotIn(provider, providers.search(safe_eval(action['domain'])))
        compatible = providers._get_compatible_providers(
            self.env.company.id, self.env.ref('base.partner_admin').id, 10.0)
        self.assertIn(provider, compatible)

    def test_action_keeps_existing_domain_and_does_not_change_record(self):
        action = self.env.ref('base.open_module_tree')
        action.domain = "[('state', '=', 'installed')]"
        result = action._get_action_dict()
        self.assertEqual(action.domain, "[('state', '=', 'installed')]")
        self.assertIn(('state', '=', 'installed'), safe_eval(result['domain']))
        self.assertIn(('to_buy', '=', False), safe_eval(result['domain']))


@tagged('erpico_debranding')
class TestSettingsView(TransactionCase):

    def test_get_views_strips_upgrade_boolean(self):
        view = self.env.ref('base_setup.res_config_settings_view_form')
        # la vista real contiene el widget en los campos Enterprise heredados
        self.assertIn('upgrade_boolean', view.arch)
        result = self.env['res.config.settings'].get_views([(view.id, 'form')])
        arch = result['views']['form']['arch']
        self.assertNotIn('upgrade_boolean', arch)
        tree = etree.fromstring(arch)
        setting = tree.xpath("//setting[@id='inter_company']")
        if setting:
            self.assertEqual(setting[0].get('invisible'), 'True')
        self.assertGreater(len(arch), 1000)


@tagged('erpico_debranding')
class TestMenus(TransactionCase):

    def test_store_menus_reparented(self):
        parent = self.env.ref('base.menu_ir_property')
        for xmlid in ('base.theme_store', 'base.menu_theme_store',
                      'base.menu_third_party'):
            self.assertEqual(self.env.ref(xmlid).parent_id.id, parent.id)


@tagged('erpico_debranding')
class TestBrandedRenders(TransactionCase):

    def test_brand_promotion_message(self):
        html = str(self.env['ir.qweb']._render('web.brand_promotion_message'))
        self.assertIn('ERPICO', html)
        self.assertNotIn('Odoo', html)
        self.assertNotIn('odoo.com', html)

    def test_mail_layout_render(self):
        message = self.env['mail.message'].search([], limit=1)
        self.assertTrue(message)
        values = {
            'message': message,
            'company': self.env.ref('base.main_company'),
            'email_notification_force_footer': True,
        }
        html = str(self.env['ir.qweb']._render(
            'mail.mail_notification_layout', values))
        self.assertIn('ERPICO', html)
        self.assertNotIn('odoo.com', html)


@tagged('erpico_debranding')
class TestDebrandingHttp(HttpCase):

    def test_database_manager_blocked(self):
        response = self.url_open('/web/database/manager')
        self.assertEqual(response.status_code, 403)

    def test_database_selector_blocked(self):
        response = self.url_open('/web/database/selector')
        self.assertEqual(response.status_code, 403)

    def test_login_debranded(self):
        response = self.url_open('/web/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Powered by <b>ERPICO</b>', response.text)
        self.assertNotIn('web/database/manager', response.text)
        self.assertIn('erpico-isotipo.png', response.text)

    def test_database_post_endpoints_blocked(self):
        """Todos los POST de gestión de BD devuelven 403 (R-001 fix)."""
        endpoints = [
            '/web/database/create',
            '/web/database/duplicate',
            '/web/database/drop',
            '/web/database/backup',
            '/web/database/restore',
            '/web/database/change_password',
        ]
        for ep in endpoints:
            response = self.url_open(ep, data={'master_pwd': 'x'})
            self.assertEqual(response.status_code, 403, ep)


@tagged('erpico_debranding')
class TestPatchMigrationParity(TransactionCase):
    """El parche se comparte con migraciones y es idempotente."""

    def test_patch_idempotent(self):
        """Segunda ejecución del parche no modifica nada."""
        from odoo.addons.erpico_debranding.patches.legacy_emails import (
            patch_legacy_emails)
        result = patch_legacy_emails(self.env)
        self.assertEqual(result, [], "Patch was not idempotent")


@tagged('erpico_debranding')
class TestBotWelcomeNeutral(TransactionCase):
    """Bienvenida del bot sin marca Odoo."""

    def test_init_odoobot_neutral(self):
        user = self.env['res.users'].create({
            'name': 'Test Debrand',
            'login': 'test_debrand_%s' % self.env.cr.now,
            'email': 'test_debrand@example.com',
            'group_ids': [(4, self.env.ref('base.group_user').id)],
        })
        channel = user._init_odoobot()
        messages = channel.message_ids
        self.assertTrue(messages)
        for msg in messages:
            self.assertNotIn('Odoo', str(msg.body))
        self.assertNotIn('odoo.com', str(channel.message_ids[0].body))
        bot = self.env.ref('base.partner_root')
        self.assertEqual(bot.name, 'ERPICO Assistant')
        self.assertTrue(bot.image_1920)
        with tools.file_open('erpico_debranding/static/src/img/bot_placeholder.png', 'rb') as image:
            expected = bot._fields['image_1920']._image_process(
                base64.b64encode(image.read()), self.env)
        self.assertEqual(bot.image_1920, expected)

    def test_get_answer_neutralizes(self):
        bot = self.env['mail.bot']
        user = self.env['res.users'].create({
            'name': 'Test Debrand Answer',
            'login': 'test_debrand_answer_%s' % self.env.cr.now,
            'email': 'test_answer@example.com',
            'group_ids': [(4, self.env.ref('base.group_user').id)],
        })
        channel = user._init_odoobot()
        user.sudo().odoobot_state = 'onboarding_command'
        answer = bot.with_user(user)._get_answer(
            channel, 'help', {'author_id': user.partner_id.id}, command='help')
        self.assertIn('@ERPICO Assistant', str(answer))
        self.assertNotIn('OdooBot', str(answer))
