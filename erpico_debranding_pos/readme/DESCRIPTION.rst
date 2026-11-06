Erpico POS Debranding
=====================

Addon de la suite de debranding ERPICO para punto de venta (POS) de Odoo 19.
Puede instalarse independientemente del addon núcleo.

Sustituye la línea "Powered by Odoo" del recibo de venta (`order_receipt.xml`)
por "Powered by ERPICO" mediante herencia QWeb. También sustituye la marca
Odoo en las dos posiciones de la pantalla de cliente del POS.

Requiere `point_of_sale`.

El recibo y la pantalla de cliente utilizan bundles separados. Las pruebas de
navegador validan los templates; la impresión física y el funcionamiento offline
requieren validación adicional con el hardware y configuración de destino.
