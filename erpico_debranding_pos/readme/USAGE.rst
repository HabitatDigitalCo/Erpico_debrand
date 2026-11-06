Uso
===

Instalar en Odoo Community 19 con ``point_of_sale`` disponible:

.. code-block:: bash

    odoo -d <base> -i erpico_debranding_pos

Para una versión ya instalada, actualizar con ``-u erpico_debranding_pos``
siguiendo el procedimiento de respaldo del entorno. Verificar el recibo y la
pantalla de cliente después de reconstruir o recargar los assets.

Las pruebas Hoot se ejecutan en una base de prueba aislada mediante
``/web/tests?headless=true&tag=erpico_debranding_pos``. Ver la especificación
en ``specs/spec-pos-receipt-v1.md`` para cobertura y límites.
