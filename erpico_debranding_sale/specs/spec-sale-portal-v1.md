# Especificación — Debranding de ventas y compras 19.0.1.1.0

## Alcance

- Mantener Ventas y Compras en el mismo addon; dependencias: `erpico_debranding`,
  `sale` y `purchase`. Instalar este addon requiere ambos módulos de negocio.
- Ocultar botón y modal `Connect with your software!` en portales de venta y
  compra, incluso cuando existen integraciones EDI.
- Ocultar en los reportes de orden y cotización de compra el enlace al modal
  que ya no se muestra.

La ocultación es visual. Los endpoints `/my/orders/<id>/download_edi` y
`/my/purchase/<id>/download_edi` no se modifican: conservan la comprobación
de acceso y los tokens de Odoo. Para prohibir EDI se necesita una política y
controles de servidor adicionales, fuera del alcance de este addon.

## Implementación

- `views/sale_portal_templates.xml`: hereda
  `sale.sale_order_portal_template` y `purchase.portal_my_purchase_order`.
- `views/purchase_report_templates.xml`: hereda
  `purchase.report_purchaseorder_document` y
  `purchase.report_purchasequotation_document`, eliminando el bloque con el
  enlace al modal.
- Los tests HTTP usan `post_install` para ejecutarse con todas las extensiones
  instaladas cargadas.

## Validación

En Odoo `19.0-20260817` y PostgreSQL 16 aislado:

- Instalación limpia de la suite: 31 pruebas Python, 0 fallos y 0 errores.
- Actualización de los dos addons desde `19.0.1.0.1`: 11 pruebas Python, sin
  fallos ni errores.
- Tests con EDI simulado comprueban que el botón aparece sin el override y
  desaparece con él; también prueban portales sin token o con token inválido.
- Los dos reportes se renderizaron a HTML con proveedor de portal y EDI
  simulado. El enlace está presente sin override y ausente con override.
- Se convirtieron esos HTML directamente a PDF con `wkhtmltopdf` y se comprobó
  el texto en ambos casos. No se validó el flujo completo de generación de PDF
  de Odoo ni el envío o impresión de esos documentos.

Repetir pruebas con integraciones EDI reales, idiomas y configuraciones del
entorno de destino. No se realizaron integraciones o pagos reales.
