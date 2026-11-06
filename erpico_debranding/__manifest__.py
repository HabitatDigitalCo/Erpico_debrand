{
    'name': 'Erpico Debranding',
    'version': '19.0.1.4.0',
    'category': 'Hidden',
    'summary': 'Remove Odoo branding from UI, emails and portal (Odoo 19)',
    'description': """
Elimina la marca Odoo / Odoo Enterprise de una base Community 19: login,
settings, portal, emails salientes, menú de usuario y bloqueo de rutas de
gestión de base de datos.

Módulo base de la suite de debranding ERPICO. Los módulos
`erpico_debranding_sale` y `erpico_debranding_pos` extienden su alcance al
portal de ventas/compra y al recibo de punto de venta.

Las acciones de catálogo se filtran en la interfaz; las operaciones internas
no se filtran. El hook modifica datos existentes de forma limitada: consulte
la documentación de respaldo y rollback antes de instalar o actualizar.
    """,
    'author': 'Habitat Digital',
    'website': 'https://github.com/Vankisito/DebrandingERPICO',
    'license': 'LGPL-3',
    'depends': [
        'web',
        'base_setup',
        'portal',
        'mail',
        'mail_bot',
        'auth_signup',
        'payment',
    ],
    'data': [
        'data/ir_ui_menu.xml',
        'views/templates.xml',
        'views/emails.xml',
        'views/portal.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'erpico_debranding/static/src/js/user_menu.js',
            'erpico_debranding/static/src/js/messaging_menu.js',
            'erpico_debranding/static/src/js/out_of_focus.js',
            'erpico_debranding/static/src/scss/debranding.scss',
            'erpico_debranding/static/src/settings_form_view/res_config_edition.js',
            'erpico_debranding/static/src/settings_form_view/res_config_edition.xml',
        ],
        'web.assets_frontend': [
            'erpico_debranding/static/src/scss/debranding.scss',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
