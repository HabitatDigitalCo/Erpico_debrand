# Cobertura de pruebas — `erpico_debranding` 19.0.1.4.0

## Ejecución automatizada del núcleo

Odoo Community `19.0-20260817`, PostgreSQL 16 aislado, base sintética nueva,
sin demo y sin cron. Resultado reportado por Odoo: **20 tests, 0 fallos y 0
errores**, 2026-11-06 UTC. Comando y precauciones:
`Manual_Pruebas_Testing.md`.

| Clase | Cobertura | Casos |
|---|---|---:|
| `TestLegacyEmails` | Cuerpos originales, asunto/cuerpo renderizados, bot estándar, protección de contacto homónimo y plantillas/nombre/imagen personalizados | 6 |
| `TestEnterpriseHidden` | Dominios de catálogo, dominio original, búsqueda/conteo ORM y compatibilidad de proveedor sintético | 3 |
| `TestSettingsView` | Eliminación del widget y, si el setting aparece, condición de ocultación | 1 |
| `TestMenus` | Reubicación de tres menús de tiendas | 1 |
| `TestBrandedRenders` | Render de promoción y layout de correo | 2 |
| `TestDebrandingHttp` | Login, manager, selector y seis POST con base seleccionada | 4 |
| `TestPatchMigrationParity` | Idempotencia del parche compartido | 1 |
| `TestBotWelcomeNeutral` | Bienvenida, avatar y respuesta de onboarding | 2 |

La prueba de ajustes comprueba la invisibilidad solo si el setting está presente;
no sustituye una revisión de todas las vistas de addons instalados.

## Upgrade y restauración

- Upgrade sintético `19.0.1.3.0` → `19.0.1.4.0`: conservó contacto homónimo,
  nombre e imagen del bot y plantilla personalizados; se verificaron asunto
  estándar y dominio del catálogo.
- La validación de recuperación debe repetirse por entorno, incluyendo base,
  filestore y pruebas de negocio; consultar el manual.

## Pendiente y límites

- Sin prueba de pago real, checkout de navegador ni integración de proveedores.
- Sin validación de traducciones distintas de `en_US`; plantillas personalizadas
  pueden conservar marca Odoo.
- Sin prueba completa de webclient tras este upgrade.
- La ejecución de 20 tests del núcleo no incluye los addons adicionales. Para
  la validación conjunta y sus límites, consultar las specs de POS y ventas.
- Las pruebas HTTP del addon no demuestran seguridad sin base seleccionada.
