# Diccionario de Recursos — `erpico_debranding`

Catálogo verbatim de todos los recursos que consume o entrega la suite
(referencias de XML/QWeb, assets, xmlids de parche). Convención de nombres:
`prefix_` = prefijo del módulo.

---

## 1. Estructura de archivos del núcleo

```
erpico_debranding/
├── __init__.py                 (post_init_hook)
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py                 (bloqueo complementario de rutas de base)
├── data/
│   └── ir_ui_menu.xml          (reparent)
├── migrations/
│   ├── 19.0.1.1.0/post-migrate.py
│   ├── 19.0.1.3.0/post-migrate.py
│   └── 19.0.1.4.0/post-migrate.py
├── models/
│   ├── __init__.py
│   ├── actions.py              (dominios de catálogo Enterprise)
│   ├── mail_bot.py
│   ├── res_users.py
│   └── res_config_settings.py  (oculta upgrade_boolean)
├── patches/
│   ├── __init__.py
│   └── legacy_emails.py        (parche idempotente)
├── readme/
│   ├── DESCRIPTION.rst
│   ├── USAGE.rst
│   ├── CONFIGURE.rst
│   ├── CONTRIBUTORS.rst
│   └── CHANGELOG.rst
├── static/src/
│   ├── img/erpico-isotipo.png
│   ├── img/bot_placeholder.png
│   ├── js/user_menu.js
│   ├── js/messaging_menu.js
│   ├── js/out_of_focus.js
│   ├── scss/debranding.scss
│   └── settings_form_view/res_config_edition.js + res_config_edition.xml
├── tests/
│   ├── __init__.py
│   └── test_debranding.py
└── views/
    ├── templates.xml
    ├── emails.xml
    └── portal.xml
```

## 2. Xmlids definidos en views

| Xmlid | Tipo | Uso |
|---|---|---|
| `erpico_debranding.web_layout_title_favicon` | template QWeb | título y favicon |
| `erpico_debranding.web_login_layout` | template QWeb | login |
| `erpico_debranding.web_brand_promotion_message` | template QWeb | promoción web |
| `erpico_debranding.portal_record_sidebar_powered_by` | template QWeb | sidebar portal |
| `erpico_debranding.mail_notification_layout_powered_by` | template QWeb | layout de correo |
| `erpico_debranding.mail_notification_light_powered_by` | template QWeb | layout ligero |
| `erpico_debranding.reset_password_email_powered_by` | template QWeb | reset password |
| `erpico_res_config_edition` | template OWL (assets) | widget About registrado como `res_config_edition` |

## 3. Templados heredados (seed) que se sobreescriben

| Template seed | Módulo padre | Override en |
|---|---|---|
| `web.login_layout` | web | `views/templates.xml` |
| `web.layout` | web | `views/templates.xml` |
| `web.brand_promotion_message` | web | `views/templates.xml` |
| `portal.portal_record_sidebar` | portal | `views/portal.xml` |
| `mail.mail_notification_layout` | mail | `views/emails.xml` |
| `mail.mail_notification_light` | mail | `views/emails.xml` |
| `auth_signup.reset_password_email` | auth_signup | `views/emails.xml` |
| `sale.sale_order_portal_template` | sale | `erpico_debranding_sale/views/sale_portal_templates.xml` |
| `purchase.portal_my_purchase_order` | purchase | `erpico_debranding_sale/views/sale_portal_templates.xml` |
| `purchase.report_purchaseorder_document` | purchase | `erpico_debranding_sale/views/purchase_report_templates.xml` |
| `purchase.report_purchasequotation_document` | purchase | `erpico_debranding_sale/views/purchase_report_templates.xml` |
| `point_of_sale.OrderReceipt` (order_receipt.xml) | point_of_sale | `erpico_debranding_pos/static/src/override/order_receipt.xml` |
| `point_of_sale.CustomerDisplay` | point_of_sale | `erpico_debranding_pos/static/src/override/customer_display.xml` |

## 4. Menús tocados (data/ir_ui_menu.xml)

| Xmlid seed | Operación |
|---|---|
| `base.theme_store` | parent_id → `base.menu_ir_property` |
| `base.menu_theme_store` | parent_id → `base.menu_ir_property` |
| `base.menu_third_party` | parent_id → `base.menu_ir_property` |

## 5. Email templates legados parcheados (LEGACY_EMAIL_XMLIDS)

| Xmlid | Plantilla | Tratamiento |
|---|---|---|
| `auth_signup.set_password_email` | Set Password | Reemplazos si el campo inglés coincide con el original |
| `auth_signup.portal_set_password_email` | Portal Set Password | Igual para el cuerpo |
| `auth_signup.mail_template_data_unregistered_users` | Unregistered | Igual para el cuerpo |
| `auth_signup.mail_template_user_signup_account_created` | Signup | Igual para el cuerpo |

El parche modifica el cuerpo inglés solo si coincide con el original upstream;
el asunto inglés estándar de `set_password_email` también se corrige si no fue
personalizado. Las plantillas personalizadas y otros idiomas pueden conservar
marca Odoo. El parche es idempotente.

## 6. Registros de datos relevantes

| Registro | Por qué importa |
|---|---|
| `base.partner_root` | se rebranda solo si corresponde a identidad estándar; se preservan personalizaciones |
| `payment.provider` con `module_to_buy=True` | ocultos en acciones de catálogo, no en búsquedas ORM |
| `ir.module.module` con `to_buy=True` | ocultos en acciones de catálogo, no en búsquedas ORM |

## 7. Assets declarados en manifest

### `erpico_debranding`
```
web.assets_backend:
  erpico_debranding/static/src/js/user_menu.js
  erpico_debranding/static/src/scss/debranding.scss
  erpico_debranding/static/src/settings_form_view/res_config_edition.xml
web.assets_frontend:
  erpico_debranding/static/src/scss/debranding.scss
```

### `erpico_debranding_pos`
```
point_of_sale.assets_prod:
  erpico_debranding_pos/static/src/override/order_receipt.xml
point_of_sale.customer_display_assets:
  erpico_debranding_pos/static/src/override/customer_display.xml
web.assets_unit_tests:
  templates de pantalla de cliente y tests Hoot de debranding
```

### `erpico_debranding_sale`
```
data:
  views/sale_portal_templates.xml
  views/purchase_report_templates.xml
```

## 8. Assets de marca importados (estáticos)

| Asset | Procedencia |
|---|---|
| `erpico-isotipo.png` | logo isotipo ERPICO (PNG) |
| `debranding.scss` | SCSS de los overrides del layout |
