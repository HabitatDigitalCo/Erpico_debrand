# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import base64

from odoo import tools

from . import controllers
from . import models
from .patches.legacy_emails import patch_legacy_emails


def _rebrand_bot_partner(env):
    """Rebrand only the stock bot identity, preserving custom names and images."""
    partner = env.ref('base.partner_root', raise_if_not_found=False)
    if not partner:
        return
    values = {}
    if partner.name == 'OdooBot':
        values['name'] = 'ERPICO Assistant'
    if partner.name in ('OdooBot', 'ERPICO Assistant'):
        with tools.file_open('mail/static/src/img/odoobot.png', 'rb') as icon:
            stock_image = partner._fields['image_1920']._image_process(
                base64.b64encode(icon.read()), env)
        if not partner.image_1920 or partner.image_1920 == stock_image:
            with tools.file_open(
                'erpico_debranding/static/src/img/bot_placeholder.png', 'rb'
            ) as icon:
                values['image_1920'] = base64.b64encode(icon.read())
    if values:
        partner.write(values)


def post_init_hook(env):
    patch_legacy_emails(env)
    _rebrand_bot_partner(env)
