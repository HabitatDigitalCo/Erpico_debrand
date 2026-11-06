# Manual de pruebas — `erpico_debranding` 19.0.1.4.0

Ejecutar instalación, upgrade y pruebas con **base y PostgreSQL aislados**,
datos sintéticos, cron deshabilitado y sin correo ni proveedor de pago real.
No ejecutar `--test-enable`, pruebas de upgrade ni métodos de gestión de bases
contra una base operativa.

## 1. Suite del núcleo

En una base sintética vacía, con Odoo 19 y el addon en `addons_path`:

```bash
odoo -d <base_qa> -i erpico_debranding \
  --without-demo --test-enable --test-tags=erpico_debranding \
  --http-port=18090 --no-http --max-cron-threads=0 --stop-after-init
```

Usar un puerto libre: aun con `--no-http`, `HttpCase` puede iniciar un servidor
de pruebas. La base QA no debe ser visible desde la instancia real. El tag
plano también selecciona tests de addons compañeros si están instalados;
para limitar por módulo consultar la configuración de tags de Odoo usada.

Resultado observado: **20 pruebas, 0 fallos y 0 errores** en instalación limpia
con Odoo `19.0-20260817`. Esto cubre únicamente el núcleo.

## 2. Validación funcional

- Apps y proveedores: probar dominio de las acciones, preservar el dominio
  previo y confirmar que `search`/`search_count` no ocultan registros.
- Pagos: con proveedor sintético marcado `to_buy`, verificar el cálculo de
  compatibilidad sin cobrar ni contactar servicios externos. Repetir pruebas
  de checkout con cada proveedor real en sandbox antes de promocionar.
- Correos: comprobar asunto y cuerpo renderizados en `en_US`, enlaces y
  conservación de contenido personalizado. No enviar correo real. Probar
  traducciones según idiomas aprobados; el español está pendiente.
- Bot: verificar partner `base.partner_root`, imagen estándar y preservación
  de nombre/imagen personalizados; un contacto homónimo debe permanecer intacto.
- Ajustes: inspeccionar arquitectura y validar que el `setting` con
  `upgrade_boolean` quede invisible.

## 3. HTTP y seguridad

En entorno aislado, verificar login 200, marca ERPICO e imagen accesible.
Con la base del addon seleccionada, comprobar manager, selector y los POST
enumerados en `controllers/main.py`. Las pruebas `HttpCase` dieron 403 con
base seleccionada; no prueban la protección global sin base.

Repetir con sesión nueva y **sin base seleccionada**, con `list_db=False`,
`dbfilter` y proxy de despliegue. Validar también `/web/database/list` y las
interfaces RPC aplicables. No ejecutar operaciones destructivas ni exponer
contraseñas en comandos, registros o capturas.

Un 403 con base seleccionada no demuestra que se bloqueen rutas globales.
El addon no sustituye la configuración externa.

## 4. Upgrade y rollback

1. Preparar base sintética con la versión anterior, contenido personalizado y
   filestore aislado. Respaldar ambos antes de actualizar.
2. Actualizar a la versión candidata; confirmar versión, datos personalizados,
   asunto original, acción de catálogo y funcionamiento del login.
3. Restaurar base **y** filestore en otro entorno aislado. Comprobar registros y
   existencia de archivos adjuntos; completar pruebas de negocio pertinentes.
4. Desinstalar o ejecutar `-u` no equivale a restaurar datos anteriores.

## 5. Validaciones complementarias

Validar webclient en navegador, traducciones, checkout en sandbox y addons de
POS/ventas cuando sean relevantes. Registrar resultados por entorno sin incluir
credenciales ni datos sensibles. Ver cobertura del núcleo en `TESTS_COVERAGE.md`.
