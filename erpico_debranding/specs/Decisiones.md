# Decisiones — Suite `erpico_debranding`

Registro de decisiones técnicas. Cada una: ¿qué?, ¿por qué?, ¿alternativas
rechazadas?, ¿impacto?

Estado de cada registro: `[x]` aceptada, `[ ]` propuesta, `[!]` revocada.

---

## D-01 — Marca dura "ERPICO" como brand del seed

- **Estado:** `[x]`
- **Qué:** todos los textos de marca se sustituyen por "ERPICO" fijo
  (hardcoded en overrides y en los reemplazos del parche de emails).
- **Por qué:** single-tenant sin necesidad de configuración; símbolos web,
  favicon e isotipo de ERPICO ya importados como assets estáticos.
- **Alternativas rechazadas:** variable de entorno / `ir.config_parameter`
  por marca (`brand_name`…) — más superficie de test sin necesidad real.
- **Impacto:** para otro cliente habría que derivar este módulo.

---

## D-02 — Logo de login estático (assets), no `company_logo`

- **Estado:** `[x]`
- **Qué:** el logo del login es un asset estático (`erpico-isotipo.png` +
  CSS), no el logo de la compañía de la UI.
- **Por qué:** la página de login no razona con la compañía/logo de forma
  uniforme en 19 Community; un asset es determinista, cacheable y
  reproducible en todas las tenant.
- **Impacto:** el `company_logo` de cada compañía no se refleja en el login.
  Documentado, asumido.

---

## D-03 — Menús de tiendas: reparent, no delete

- **Estado:** `[x]`
- **Qué:** `base.theme_store`, `base.menu_theme_store` y
  `base.menu_third_party` se mueven bajo `base.menu_ir_property` (fuera de
  cualquier raíz visible de apps). No se eliminan registros.
- **Por qué:** eliminar registros del seed rompe dependencias y complica
  upgrades; el reparent conserva los registros, pero requiere rollback explícito.
- **Impacto:** visibles a administradores que expandan la jerarquía raw;
  asumido. La desinstalación no restaura automáticamente el padre previo.

---

## D-04 — Emails legados: parche en `post_init_hook` + migración

- **Estado:** `[x]`
- **Qué:** los 4 `mail.template` de `auth_signup` con `body_html` almacenado
  con marca Odoo se procesan en `patches/legacy_emails.py`. Desde `19.0.1.4.0`,
  el parche compara cada campo en inglés con su original upstream antes de
  escribir y preserva contenido personalizado. También corrige el asunto inglés
  original de invitación. El hook y las migraciones reutilizan el helper.
- **Por qué:** son campos almacenados; el QWeb solo debranda lo dinámico.
- **Alternativas rechazadas:** regenerar los templates desde XML con
  `force_create` / retrocompat bad; cambiar el correo por completo rompe
  el body del cliente.
- **Impacto:** parche idempotente (2ª ejecución = 0 patcheos), mantiene
  estructura original del body. El contenido 100% personalizado sigue siendo
  del cliente.

---

## D-05 — Renombrar partner `OdooBot` → `ERPICO Assistant`

- **Estado:** `[x]`
- **Qué:** el hook y la migración localizan `base.partner_root` y renombran
  solo su nombre estándar. Se preservan nombre e imagen personalizados.
- **Por qué:** aparece como autor/remitente en chatter, emails y archivos.
- **Detalle:** el partner del bot está marcado `active=False`; las búsquedas
  por defecto no lo ven (`ERPICO Assistant` no aparece en search normal hasta
  el cambio).

---

## D-06 — Rutas de BD: bloqueo complementario

- **Estado:** `[x]` como bloqueo complementario; protección global pendiente
  de configuración. Desde `19.0.1.2.0` también se bloquean los POST cuando se
  carga el controlador del addon; `/web/database/list` sigue sin sobrescribirse.
- **Qué:** con base seleccionada, el controlador también rechaza los seis POST
  de gestión enumerados en `controllers/main.py`. Sin base seleccionada, el
  controlador puede no cargarse; `/web/database/list` no se sobrescribe.
- **Riesgo:** no constituye control global: requieren validación `list_db`,
  `dbfilter`, proxy y aislamiento de infraestructura.

---

## D-07 — `get_views` strip de `upgrade_boolean` en settings

- **Estado:** `[x]`
- **Qué:** `res.config.settings.get_views` recorre los archs form de
  res.config.settings y elimina `widget="upgrade_boolean"` con lxml
  (XPath por atributo), antes de devolverlos.
- **Por qué:** en Community los widgets de "Upgrade" apuntan a la tienda de
  Odoo; debranding exige quitarlos de la UI.
- **Alternativas rechazadas:** editar views del seed (prohibido), JS de
  stripping en cliente (frágil y visible en flash de UI).
- **Impacto:** desde `19.0.1.4.0`, además se oculta el `setting` que contiene
  el campo, o el campo si no tiene `setting`; el campo no se elimina.

---

## D-08 — Suite de tests en el módulo núcleo

- **Estado:** `[x]`
- **Qué:** `erpico_debranding/tests/` con clases `@tagged('erpico_debranding')`
  (TransactionCase + HttpCase) que cubren parte de las superficies del núcleo.
- **Por qué:** validación reproducible fuera de sesiones HTTP manuales;
  requisito de calidad OCA.
- **Impacto:** la suite ayuda a detectar regresiones; no sustituye pruebas de
  navegador, infraestructura, traducciones o integraciones reales.

---

## D-09 — Metadatos OCA

- **Estado:** `[x]`
- **Qué:** manifests con orden canónico de claves OCA, `license: LGPL-3`,
  `author: 'Habitat Digital'`, `website` apuntando al repo GitHub.
  `readme/` con fragments `DESCRIPTION`, `USAGE`, `CONFIGURE`,
  `CONTRIBUTORS`, `CHANGELOG`. Headers de copyright y licencia en todo
  archivo fuente.
- **Por qué:** compatibilidad con pipelines OCA/`oca-addons-repo-template`,
  Pylint de la comunidad y consumo humano/agentes del `readme/`.
- **Impacto:** el proyecto es publicable tal cual.

---

## D-10 — Push notifications: se mantienen

- **Estado:** `[x]`
- **Qué:** el push permiso banner ("Turn on notifications",
  `notificationRequest` en `messaging_menu_patch.js`) **no** se elimina.
- **Por qué:** decisión del cliente — solo falta la marca, no la
  funcionalidad; el permiso de notificaciones es útil en la app.
- **Impacto:** en el tab Notificaciones sigue la card push cuando
  `mail.notification.permission === 'prompt'`.

---

## D-11 — Avatar del bot: placeholder genérico, no isotipo

- **Estado:** `[x]`
- **Qué:** el bot interno (partner `base.partner_root`) pasa a llamarse
  "ERPICO Assistant" y su imagen es un placeholder genérico
  (`bot_placeholder.png`: fondo morado `#714B67`, letra "E"), ve
  cupo del `odoobot.png` de Odoo.
- **Por qué:** un isotipo de marca para el bot sería un uso incorrecto del
  isotipo; el placeholder es neutro y no evoca Odoo.
- **Impacto:** el avatar se ve en chatter, usuarios del chat y notificación
  del sistema (fallback en `out_of_focus_service`).

---

## D-12 — Conversación del bot: neutra, no mutilada

- **Estado:** `[x]`
- **Qué:** la conversación del bot se **conserva** íntegra (onboarding de
  emoji, archivos, comandos, ping, respuestas rápidas). Solo se reemplazan
  las cadenas que citan la marca: `@OdooBot`→`@ERPICO Assistant`, "Enjoy
  exploring Odoo!"→"Enjoy exploring ERPICO!" y los links a
  `odoo.com/documentation` y `odoo.com/slides` (se vacían).
- **Por qué:** desactivar el bot (estado `disabled`) rompería el flujo de
  onboarding del core y dejaría el chat muerto; se prefiere un bot funcional
  con texto neutro.
- **Alternativas rechazadas:** estado `disabled` (ROM: sin newsletter), bot
  con texto 100% custom (más superficie de test sin necesidad).
- **Impacto:** el bot responde igual que el core; solo cambia el texto de
  marca.

---

## D-13 — Banner "Install Odoo": neutralizar en el punto único del componente

- **Estado:** `[x]`
- **Qué:** `MessagingMenu.prototype.canPromptToInstall → false` y
  `user_menuitems.remove('install_pwa')`.
- **Por qué:** el banner `installationRequest` y el +1 del `counter` se
  gobiernan por `canPromptToInstall`; un getter único lo neutraliza todo
  en un solo punto, sin tocar el push ni el resto del menú.
- **Alternativas rechazadas:** parche de toda la card `installationRequest`
  (más código, mismo resultado), ocultar vía CSS (frágil y visible en flash).
- **Impacto:** "Install Odoo" y duplicado "Install App" desaparecen;
  el navegador solo muestra su prompt nativo si el JS llama `pwa.show()`,
  lo que ya no sucede.

---

## D-14 — About robusto: componente propio con template único

- **Estado:** `[x]`
- **Qué:** en vez de confiar en sobrescribir `res_config_edition` por mismo
  `t-name`, se registra un componente **propio** (`ErpicoResConfigEdition`,
  template `erpico_res_config_edition`) bajo la misma clave de
  `view_widgets` → el add del registry gana por orden de carga del bundle.
- **Por qué:** la sobrescritura por t-name idéntico puede perder según el
  orden de los assets; registrar el widget (que referencia su propio
  template con nombre único) es determinista.
- **Impacto:** la tarjeta About muestra "ERPICO / Powered by ERPICO", sin
  versión Community ni copyright Odoo.

---

## D-15 — Enterprise oculto solo en presentación

- **Estado:** `[x]` desde `19.0.1.4.0`.
- **Qué:** se añaden dominios a acciones de listado de módulos y proveedores;
  ajustes con `upgrade_boolean` se ocultan. Se retiraron filtros globales ORM.
- **Por qué:** evitar alterar selección de proveedores y operaciones internas.
- **Límite:** no es seguridad, no cubre necesariamente todos los accesos ni
  garantiza que cada contador de interfaz excluya Enterprise.

## D-16 — Preservar datos personalizados

- **Estado:** `[x]` desde `19.0.1.4.0`.
- **Qué:** se identifica el bot por XML ID y solo se modifica su identidad
  estándar; los campos de correo en inglés se cambian solo si coinciden con
  sus valores originales. Un contacto homónimo no cambia.
- **Límite:** contenido personalizado y otros idiomas pueden mostrar marca Odoo;
  cambios persistidos previamente requieren recuperación desde respaldo.

## D-17 — Seguridad de base en infraestructura

- **Estado:** `[x]` como límite de arquitectura; configuración externa pendiente.
- **Qué:** el controlador es complemento de `list_db=False`, `dbfilter`, proxy
  y aislamiento. No se considera cobertura global para peticiones sin base.
- **Verificación:** probar rutas con y sin base seleccionada en cada entorno;
  no asumir que un 403 en una sesión protegida aplica a peticiones sin base.
