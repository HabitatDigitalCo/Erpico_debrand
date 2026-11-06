# ERPICO Debranding — Suite para Odoo 19

Suite de debranding de marca para Odoo 19 Community Edition. Adapta superficies
de interfaz, portal y correo a **ERPICO** y oculta opciones Enterprise en los
catálogos compatibles. Las plantillas personalizadas y traducciones pueden
conservar referencias a Odoo; revisar cada entorno antes de su publicación.

## Módulos

| Módulo | Versión | Alcance |
|---|---|---|
| `erpico_debranding` | 19.0.1.4.0 | Núcleo: login, settings, portal, emails, menú de usuario, filtros de interfaz Enterprise y bloqueo complementario de rutas de BD |
| `erpico_debranding_sale` | 19.0.1.1.0 | Oculta conexión EDI en portales de ventas/compras y enlaces relacionados en reportes de compra |
| `erpico_debranding_pos` | 19.0.1.1.0 | Marca ERPICO en recibo POS y pantalla de cliente |

## Documentación

Cada módulo es autocontenido: su especificación vive dentro de su propia
carpeta en `specs/` (estructura copiada del proyecto de referencia
`GpoBCA_Seguros-desarrollo`):

- `erpico_debranding/specs/` — decisiones, changelog,
  bugs, cobertura de tests, arquitectura, lógica, BDD, diccionario de
  recursos, manual de pruebas y specs de parches.
- [`erpico_debranding_sale/specs/spec-sale-portal-v1.md`](erpico_debranding_sale/specs/spec-sale-portal-v1.md) — portal y reportes de ventas/compras.
- [`erpico_debranding_pos/specs/spec-pos-receipt-v1.md`](erpico_debranding_pos/specs/spec-pos-receipt-v1.md) — recibo y pantalla de cliente POS.

## Estándares

Los tres módulos siguen convenciones **OCA** (Odoo Community Association):

- Manifest con orden canónico de claves y `license: LGPL-3`.
- Documentación de descripción, uso, configuración y cambios en `readme/`.
- Headers de copyright `LGPL-3.0 or later` en todo archivo fuente.
- Suite de tests con `@tagged('erpico_debranding')` + cobertura `HttpCase`.

## Instalación

Respaldar base y filestore antes de instalar o actualizar. El addon no sustituye
`list_db=False`, `dbfilter` ni las restricciones del proxy; desinstalar no
revierte automáticamente datos existentes modificados. Consultar
`erpico_debranding/readme/CONFIGURE.rst`.

```bash
odoo -d <base> -i erpico_debranding
```

Instalar las extensiones necesarias:

```bash
odoo -d <base> -i erpico_debranding_pos,erpico_debranding_sale
```

`erpico_debranding_pos` requiere `point_of_sale`;
`erpico_debranding_sale` requiere `erpico_debranding`, `sale` y `purchase`.
Odoo instalará las dependencias que falten: revisar su impacto antes de ejecutar
el comando. Para actualizar instalaciones existentes, usar `-u` en lugar de
`-i` y seguir el procedimiento de respaldo y validación del entorno.

## Pruebas

En una base sintética aislada, con los addons disponibles en `addons_path`:

```bash
odoo -d <base_qa> -i erpico_debranding,erpico_debranding_pos,erpico_debranding_sale \
  --without-demo --test-enable --test-tags=erpico_debranding \
  --http-port=<puerto_libre> --max-cron-threads=0 --stop-after-init
```

El tag plano selecciona pruebas de los tres addons. La prueba de navegador POS
se ejecuta aparte; consultar su especificación. Nunca ejecutar esta instalación
de prueba ni generar documentos sintéticos en una base operativa.

## Licencia

LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
