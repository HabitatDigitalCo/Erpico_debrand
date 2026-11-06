Uso
===

Instalar en Odoo Community 19:

.. code-block:: bash

    odoo -d <base> -i erpico_debranding_sale

Odoo instalará las dependencias ``erpico_debranding``, ``sale`` y ``purchase``
que falten. Para una versión ya instalada, actualizar con
``-u erpico_debranding_sale`` siguiendo el procedimiento de respaldo del entorno.

Validar portales de venta y compra y los dos reportes de compra. Cuando EDI esté
disponible, el botón, modal y enlaces correspondientes no se mostrarán. Los
endpoints EDI no se desactivan; la ocultación no es un control de seguridad.
