# APP-INVENTARIO · El Manzano

Panel web de diferencias de inventario (Ferretería Oviedo · El Manzano).

**SPA 100% cliente** — sin backend, sin login, sin servidor. Toda la lógica corre en el navegador.
Los datos cargados se guardan en IndexedDB del navegador del dispositivo (no se sincronizan entre dispositivos).

## Uso online

https://oviedoem.github.io/APP-INVENTARIO/

## Uso local

Doble clic en `index.html` (o `python -m http.server 8000` desde la carpeta y abrir http://localhost:8000).

## Estructura

- `index.html` — UI
- `app.js` — lógica
- `style.css` — estilos
- `planos_generated.js` — HTML de planos pre-renderizado (regenerado por `generar_planos.js` cuando cambien los Excel de planos)

## Datos

Los Excel de inventario (`Inventario 2025.xlsx`, `Inventario 2026.xlsx`, `Planos*.xlsx`) **no se versionan** — viven solo localmente en cada PC.

## Persistencia

Al recargar la app, si hay datos previos en IndexedDB se muestra un banner para restaurar la sesión o empezar de cero. El botón 🧹 Limpiar del header borra todo (IDB + localStorage + memoria).

> **Nota:** IndexedDB y localStorage son por dispositivo y por navegador. Si Pedro carga datos en su PC, su celular arranca vacío — no hay sincronización entre dispositivos.
