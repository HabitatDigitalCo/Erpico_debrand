Erpico Debranding
=================

Módulo de debranding ERPICO para Odoo 19 Community. Adapta superficies de
interfaz, portal y correo. El recibo POS y el portal de ventas/compras requieren
sus addons compañeros.

La marca del producto es **ERPICO**: la línea "Powered by Odoo" se sustituye
por "Powered by ERPICO" en las superficies implementadas y verificadas.
Plantillas personalizadas y otros idiomas pueden conservar marca Odoo.

Alcance:

- Página de login: título, favicon, footer y enlaces de marca.
- Footer web y portal.
- Menú Apps: oculta módulos de Odoo Enterprise (``to_buy``) y las tiendas de
  apps.
- Tarjeta "About" de Ajustes y widgets de upgrade.
- Menú de usuario: elimina los elementos Support, Odoo.com Account e Install App.
- Emails salientes (layouts de correo y plantillas de ``auth_signup``).
- Botón "Connect with your software!" del portal (módulo compañero
  ``erpico_debranding_sale``).
- Recibo de venta POS (módulo compañero ``erpico_debranding_pos``).
- Bloqueo complementario de rutas de gestión de bases con la base seleccionada.

Depende de módulos core (web, base_setup, portal, mail, auth_signup,
payment) y no modifica el código upstream. Algunos datos existentes se
modifican: ``-u`` o la desinstalación no restauran automáticamente los valores
anteriores. La seguridad de rutas de bases depende también de la infraestructura.
