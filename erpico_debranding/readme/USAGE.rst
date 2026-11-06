Usage
=====

Instalar el módulo en una base Community 19:

.. code-block:: bash

    odoo -d <base> -i erpico_debranding

El debranding es inmediato tras la instalación:

- Página de login: título y favicon **ERPICO**, logo isotipo, footer
  "Powered by ERPICO" y sin enlace a gestión de bases de datos.
- Catálogos de Apps y proveedores de pago: las acciones de listado ocultan
  registros marcados Enterprise. Las búsquedas internas y los pagos no se filtran.
  Esto es presentación, no un control de acceso.
- Ajustes: la tarjeta "About" se reemplaza y las opciones con el widget
  ``upgrade_boolean`` se ocultan.
- Portal/web: footer "Powered by ERPICO".
- Emails: layouts dinámicos y plantillas inglesas originales se debrandan.
  Las plantillas personalizadas se conservan y pueden contener marca Odoo;
  otros idiomas requieren validación y adaptación independiente.
- Con la base del addon seleccionada, el controlador rechaza las rutas de
  gestión de bases enumeradas en ``controllers/main.py``. Sin base seleccionada
  puede no cargarse; ``/web/database/list`` no se modifica.

Para el portal de ventas/compra y el recibo POS, instalar además los módulos
compañeros:

.. code-block:: bash

    odoo -d <base> -i erpico_debranding_sale
    odoo -d <base> -i erpico_debranding_pos

Para revertir cambios persistentes en plantillas, avatar o menús, usar un
respaldo previo de base y filestore: desinstalar o ejecutar ``-u`` no restaura
automáticamente los valores anteriores.
