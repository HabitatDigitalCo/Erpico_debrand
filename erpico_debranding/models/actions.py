# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    def _get_action_dict(self):
        """Filter catalog actions, without changing business ORM searches."""
        result = super()._get_action_dict()
        field = {
            'ir.module.module': 'to_buy',
            'payment.provider': 'module_to_buy',
        }.get(result.get('res_model'))
        if field and not result.get('res_id'):
            domain = result.get('domain') or '[]'
            if not isinstance(domain, str):
                domain = repr(domain)
            result['domain'] = '(%s) + %r' % (domain, [(field, '=', False)])
        return result
