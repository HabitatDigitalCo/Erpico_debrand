Changelog
=========

19.0.1.1.0
----------
* Oculta en los reportes de compra los enlaces al modal EDI oculto.
* Verifica con EDI sintético que los botones aparecerían sin el addon, pero
  no aparecen con sus overrides; prueba acceso al portal sin token válido.
* Ejecuta pruebas HTTP tras cargar todos los módulos instalados.
* Valida instalación limpia y actualización desde 19.0.1.0.1 en Odoo 19.

19.0.1.0.1 (2026-09-18)
-----------------------
* Test automatizados del portal (HttpCase sale y purchase) que verifican la
  ausencia de "Connect with your software!" y del modal asociado.

19.0.1.0.0 (2026-09-17)
-----------------------
* Versión inicial: oculta "Connect with your software!" en el portal de
  ventas/compra.
