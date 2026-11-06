# Arquitectura — `erpico_debranding` 19.0.1.4.0

Addon núcleo para Odoo Community 19. Adapta presentación y ciertos datos de
marca; no es frontera de seguridad ni aislamiento SaaS. Los addons de POS y
portal de ventas/compras son independientes y requieren validación propia.

## Acciones y ajustes

| Archivo | Comportamiento |
|---|---|
| `models/actions.py` | En `_get_action_dict`, agrega `to_buy=False` a acciones de listado de `ir.module.module` y `module_to_buy=False` a listados de `payment.provider`, conservando el dominio existente. No modifica la acción persistida. |
| `models/res_config_settings.py` | En las arquitecturas de ajustes, oculta el `setting` que contiene un campo `upgrade_boolean` —o el campo si no hay `setting`— y elimina el atributo del widget. |
| `data/ir_ui_menu.xml` | Reubica tres menús nativos de tiendas; es un cambio persistente en registros existentes. |

Los filtros aplican a las acciones descritas, no a toda entrada posible de UI,
RPC o vistas de un solo registro. No filtran `search`, `search_fetch`,
`search_count` ni el cálculo de proveedores compatibles; tampoco constituyen
ACL o record rules. El antiguo contexto `debranding_show_enterprise` y los
overrides globales de `models/base.py` ya no forman parte del código fuente.

## Marca y presentación

- `views/templates.xml`, `views/portal.xml` y `views/emails.xml`: herencias
  QWeb de login, portal y layouts dinámicos de correo.
- `static/src/js/` y `static/src/settings_form_view/`: menú de usuario,
  notificaciones y tarjeta About; se cargan mediante assets del manifest.
- `models/mail_bot.py` y `models/res_users.py`: mensajes del bot. Los textos
  que dependen de traducciones deben probarse por idioma.

## Datos persistentes y migración

El `post_init_hook(env)` llama a `patch_legacy_emails(env)` y
`_rebrand_bot_partner(env)`. Las migraciones reutilizan esos helpers, incluida
`19.0.1.4.0/post-migrate.py` para la actualización correspondiente.

- El parche de correo compara la plantilla inglesa almacenada con el original
  de `auth_signup`: modifica el cuerpo solo si coincide con el original y el
  asunto solo si coincide con el original. Si ya está parcheado no repite la
  escritura; no reescribe cuerpos o asuntos personalizados.
- La identidad del bot se localiza por `base.partner_root`. Se respetan nombre
  e imagen personalizados; el avatar se sustituye solo si está vacío o coincide
  con el original y el nombre es el estándar o el de ERPICO.
- Los cambios históricos ya aplicados no se revierten automáticamente con
  `-u` ni al desinstalar. La recuperación requiere respaldo adecuado y proceso
  de restauración validado.

## Rutas de base de datos

`controllers/main.py` hereda `web.Database`: bloquea manager y selector y los
POST create, duplicate, drop, backup, restore y change_password **cuando Odoo
carga este addon para la base de la petición**. No sobrescribe
`/web/database/list`. Sin base seleccionada, las rutas globales de Odoo pueden
atender la petición sin cargar este controlador.

Aplicar y probar controles externos: `list_db=False`, `dbfilter` restrictivo,
proxy y aislamiento de infraestructura.

## Referencias

- Estado de pruebas y límites: `TESTS_COVERAGE.md`.
- Procedimiento de QA: `Manual_Pruebas_Testing.md`.
- Historial de cambios: `Changelog.md`.
