{
    'name': 'Erpico POS Debranding',
    'version': '19.0.1.1.0',
    'category': 'Hidden',
    'summary': 'Remove Odoo branding from POS receipts',
    'description': """
Reemplaza la marca Odoo por ERPICO en el recibo y la pantalla de cliente del
punto de venta (POS) de Odoo 19.
    """,
    'author': 'Habitat Digital',
    'website': 'https://github.com/Vankisito/DebrandingERPICO',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale.assets_prod': [
            'erpico_debranding_pos/static/src/override/order_receipt.xml',
        ],
        'point_of_sale.customer_display_assets': [
            'erpico_debranding_pos/static/src/override/customer_display.xml',
        ],
        'web.assets_unit_tests': [
            'point_of_sale/static/src/customer_display/customer_display.xml',
            'erpico_debranding_pos/static/src/override/customer_display.xml',
            'erpico_debranding_pos/static/tests/**/*.test.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
}
