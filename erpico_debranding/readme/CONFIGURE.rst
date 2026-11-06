Configuration
=============

El addon no crea parámetros de sistema ni grupos. Los filtros Enterprise son
de interfaz, no reemplazan permisos ni reglas de acceso.

Para un despliegue SaaS, configurar y verificar fuera del addon ``list_db=False``,
``dbfilter`` restrictivo, proxy y aislamiento por tenant. El controlador del
addon no garantiza protección cuando no hay base seleccionada. No modificar
configuración de infraestructura sin validación del equipo responsable.

Antes de instalar o actualizar, respaldar base y filestore y probar la
restauración en un entorno aislado. La desinstalación no revierte automáticamente
los datos preexistentes modificados por el addon o versiones anteriores.
