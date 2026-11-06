# Lógica de debranding — `erpico_debranding` 19.0.1.4.0

## Flujo

1. Una acción de ventana para `ir.module.module` o `payment.provider` recibe
   un dominio adicional que oculta registros marcados Enterprise en el listado.
   La acción almacenada y las búsquedas internas no se modifican.
2. Al solicitar vistas de `res.config.settings`, las opciones que contienen
   `upgrade_boolean` se ocultan en la arquitectura devuelta.
3. QWeb, JS y SCSS adaptan login, portal, correo dinámico y elementos de UI.
4. Al instalar o migrar, los helpers tratan solo plantillas originales inglesas
   y el partner identificado por `base.partner_root`; respetan personalizaciones.

## Reglas

- Ocultar no es seguridad. ACL, permisos, infraestructura y proxy son controles
  independientes.
- Los filtros son de acciones de listado; no deben afectar compatibilidad de
  proveedores, procesos de pago ni otras consultas del ORM.
- `patches/legacy_emails.py` compara el contenido en `en_US` con la definición
  upstream antes de escribir. No garantiza debranding de plantillas
  personalizadas o traducciones.
- El nombre personalizado del bot se preserva; su imagen personalizada tampoco
  se reemplaza. Una imagen estándar se sustituye solo para el nombre estándar
  o ERPICO.
- El controlador de base depende de que el addon esté cargado para la base de
  la petición. No garantiza bloqueo en solicitudes sin base seleccionada.
- Instalar, actualizar o desinstalar puede dejar cambios persistentes en correo,
  bot y menús; un upgrade no es rollback.

Para detalle de archivos y pruebas ver `Arquitectura_ERPICO_Debranding.md` y
`TESTS_COVERAGE.md`.
