# Auditoría App Inventario — 2026-11-04

## Estado y evidencia

- Último log: `E:\CONOCIMIENTO DEL NEGOCIO\control-center\registro\logs\appinventario\2026-10-16_181836_ok.log`.
- Estado previo: repo limpio, rama `main`, HEAD `5c1fda2`, remoto `oviedoem/APP-INVENTARIO`; no se hizo git.
- `py_compile` aplicable y `node --check` para `app.js` y `generar_planos.js`: OK; no se ejecutó el generador.
- El `.bat` publica con `git add/commit/pull/push`; quedó sin ejecutar.
- `node_modules` se conserva como dependencia local de SheetJS/xlsx. `planos_generated.js` es artefacto vigente generado desde el Excel de planos; no se tocó.

## Flujo

SPA cliente sin backend: carga XLSX/CSV con SheetJS/PapaParse, guarda datasets en IndexedDB y estado pequeño en localStorage, y exporta informes XLSX desde el navegador. `generar_planos.js` lee el Excel de planos de ejemplo y escribe `planos_generated.js`; no ejecutarlo sin cambio aprobado.

## Riesgos y mejoras

- Riesgos: `node_modules` no debe entrar al repo; `planos_generated.js` debe sincronizarse con el código consumidor; los Excel reales son locales.
- Mejoras seguras: comprobar dependencias/archivos sensibles antes de publicar; documentar fecha/origen del Excel de planos; verificar hash/tamaño tras una regeneración aprobada.
