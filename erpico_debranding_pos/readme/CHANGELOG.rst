Changelog
=========

19.0.1.1.0
----------
* Sustituye la marca Odoo en la pantalla de cliente, en su bundle propio.
* Añade pruebas de render en navegador para venta, devolución, recibo
  simplificado y pantalla de cliente; verifica registro en bundles normal
  y oscuro, sin validar visualmente el modo oscuro.
* Valida instalación limpia y actualización desde 19.0.1.0.1 en Odoo 19.

19.0.1.0.1 (2026-09-18)
-----------------------
* Test automatizados del recibo: override registrado en assets
  (``_get_asset_paths``) y contenido de ``order_receipt.xml``.

19.0.1.0.0 (2026-09-17)
-----------------------
* Versión inicial: reemplaza "Powered by Odoo" por "Powered by ERPICO" en el
  recibo de POS.
