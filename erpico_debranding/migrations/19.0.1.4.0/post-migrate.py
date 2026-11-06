# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import SUPERUSER_ID, api
from odoo.addons.erpico_debranding import _rebrand_bot_partner
from odoo.addons.erpico_debranding.patches.legacy_emails import patch_legacy_emails


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    patch_legacy_emails(env)
    _rebrand_bot_partner(env)
