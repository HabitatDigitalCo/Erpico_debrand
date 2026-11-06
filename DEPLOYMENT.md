# Estrategia de Ramas y Deploy — DebrandingERPICO

**Proyecto:** Debranding ERPICO — Odoo 19 Community
**Modelo:** ramas por entorno con pull desde cada servidor

---

## 1. Ramas

| Rama | Entorno | Uso |
|---|---|---|
| `develop` | Desarrollo | Integración diaria; trabajo de módulos en progreso |
| `staging` | Staging | Pre-producción; validación antes de producir |
| `production` | Producción | Solo código validado y liberado |
| `main` | — | Rama oficial de integración / estable del repositorio |

`main` es el punto de partida de las tres ramas de entorno. Todo el código
liberado debe llegar a `production` pasando por `develop` → `staging`.

## 2. Flujo de liberación

1. Desarrollo en `develop` (o ramas de tarea que se integran a `develop`).
2. Cuando un conjunto de cambios está listo, `develop` se promueve a `staging`
   (merge de `develop` en `staging`). Validación en el entorno de Staging.
3. Cuando la validación pasa, `staging` se promueve a `production`
   (merge de `staging` en `production`).
4. `main` se mantiene actualizado con lo liberado (merge de `production`
   en `main`, o se usa como integración estable).

Promoción típica:

```bash
# develop → staging
git checkout staging && git pull
git merge develop
git push

# staging → production
git checkout production && git pull
git merge staging
git push
```

## 3. Deploy por entorno (módulos Odoo)

Este repositorio contiene **solo el código de los addons**:

- `erpico_debranding`
- `erpico_debranding_sale`
- `erpico_debranding_pos`

El despliegue efectivo a cada servidor Odoo se hace fuera del repositorio
(hay infraestructura propia: Docker Compose u otra). Cada entorno apunta su
`addons_path` (o volumen) a la copia de trabajo de su rama y actualiza con:

```bash
git fetch origin
git checkout <rama-del-entorno>   # develop | staging | production
git pull --ff-only origin <rama-del-entorno>
```

Luego se aplica la actualización de los módulos en la instancia Odoo del
entorno, respaldando antes base y filestore (ver `README.md`):

```bash
odoo -d <base> -u erpico_debranding,erpico_debranding_sale,erpico_debranding_pos
```

Reglas por entorno:
- **Nunca** hacer merge directo a `staging` o `production` sin pasar por el
  flujo de promoción anterior.
- Respadar base y filestore antes de cada actualización en Staging y
  Producción.
- Los servidores de cada entorno no están definidos en este repositorio;
  su provisión y acceso se gestionan aparte.

## 4. Notas

- `PRD_MODULO_GOBIERNO_SEGURIDAD_TENANT.md` es documentación local y no se
  versiona en estas ramas.
- Convención de commits: Conventional Commits (ver historial de `main`).
