# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import SUPERUSER_ID, api
from odoo.addons.erpico_debranding import _rebrand_bot_partner


def migrate(cr, version):
    _rebrand_bot_partner(api.Environment(cr, SUPERUSER_ID, {}))
