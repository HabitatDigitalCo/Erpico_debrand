# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import SUPERUSER_ID, api
from odoo.addons.erpico_debranding.patches.legacy_emails import patch_legacy_emails


def migrate(cr, version):
    patch_legacy_emails(api.Environment(cr, SUPERUSER_ID, {}))
