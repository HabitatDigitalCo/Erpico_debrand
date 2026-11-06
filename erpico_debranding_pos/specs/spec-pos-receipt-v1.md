# Especificación — Debranding POS 19.0.1.1.0

## Alcance

- Sustituir el pie `Powered by Odoo` del recibo por `Powered by ERPICO`.
- Sustituir las dos referencias al logo Odoo en la pantalla de cliente por
  `ERPICO`, sin alterar el logo propio de la compañía.
- Odoo Community 19; dependencia declarada: `point_of_sale`.

## Implementación

- `static/src/override/order_receipt.xml` extiende
  `point_of_sale.OrderReceipt` en `point_of_sale.assets_prod`. El bundle oscuro
  de Odoo incluye el bundle de producción.
- `static/src/override/customer_display.xml` extiende
  `point_of_sale.CustomerDisplay` en `point_of_sale.customer_display_assets`.
- `static/tests/debranding.test.js` contiene pruebas Hoot del componente real
  de recibo y del template de pantalla de cliente montado con un componente de
  prueba. Los datos POS son sintéticos.

## Validación

En Odoo `19.0-20260817` y PostgreSQL 16 aislado:

- Instalación limpia de la suite: 31 pruebas Python, 0 fallos y 0 errores.
- Actualización de los dos addons desde `19.0.1.0.1`: 11 pruebas Python, sin
  fallos ni errores.
- Seis pruebas Hoot en navegador: recibo de venta, devolución y recibo
  simplificado; pantalla de cliente en estados inicial, con venta y finalizado.
  Se verificaron 22 aserciones.
- Registro del override en los bundles POS normal, oscuro y pantalla de cliente;
  el test de bundle oscuro no verifica su apariencia visual.

El render de componentes no sustituye una venta completa, la impresión física,
el envío de recibos ni la validación offline. Probar hardware, impresoras y
operaciones fiscales del entorno antes de producción.

La ejecución general de pruebas frontend de Odoo no se completó: se observó
un fallo en una prueba nativa de fecha/hora. El resultado de seis pruebas
corresponde solo al tag de este addon, no a toda la suite frontend de Odoo.

## Ejecución de pruebas frontend

Con una base de prueba aislada que tenga `erpico_debranding_pos` instalado,
acceder al runner de Odoo:

```text
/web/tests?headless=true&tag=erpico_debranding_pos
```

Ejecutar solo con datos sintéticos y un usuario autorizado para pruebas.
El bundle de tests incluye los templates de recibo y pantalla de cliente.
