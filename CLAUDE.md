# CLAUDE.md — App Inventario · El Manzano
# Cargado automáticamente al inicio de cada sesión de Claude Code.

## LEER OBLIGATORIO ANTES DE CUALQUIER TAREA

1. Leer `AGENTS.md` (reglas anti-retroceso, checklist por tipo de cambio, arquitectura de vistas)
2. Leer `MEMORIA_PROYECTO.md` si existe estado reciente
3. **REGLA FLUJO ACTUAL:** Revisar fechas de modificación en la raíz — los archivos más recientes marcan el flujo actual, no solo los `.md`.
   ```powershell
   Get-ChildItem "E:\APP-INVENTARIO" -File | Sort-Object LastWriteTime -Descending | Select-Object Name, LastWriteTime | Select-Object -First 15
   ```
4. Recién después ejecutar cualquier tarea

> **Git ownership:** Si `git status` lanza error "dubious ownership", ejecutar una vez:
> `E:\git-portable\mingw64\bin\git.exe config --global --add safe.directory E:/APP-INVENTARIO`

---

## STACK Y DIRECTORIO

- **Proyecto activo:** `E:\APP-INVENTARIO\` — trabajar SIEMPRE aquí
- **Deploy:** GitHub Pages → `https://oviedoem.github.io/APP-INVENTARIO/`
- **Commit:** `ACTUALIZAR_GITHUB_APP_INVENTARIO.bat`
- **Stack:** HTML/CSS/JS Vanilla · SPA 100% cliente · sin backend · sin login · sin servidor
- **Almacenamiento:** IndexedDB del navegador (no se sincroniza entre dispositivos)
- **Librerías:** PapaParse 5.4.1 (CSV) · Chart.js 4.4.3 (gráficos)
- **Node.js:** `E:\nodejs-portable\node.exe` (para generar_planos.js)

## REGLAS CRÍTICAS

### Nunca hacer esto
- Agregar backend, login o servidor — es SPA pura por diseño
- Diagnosticar datos (patentes, zonas) sin verificar primero en el Excel real
- Reemplazar funciones de render sin verificar que `const PLANO_SHEETS` sigue presente en app.js
- Modificar más de una función por prompt (un prompt = una función tocada)
- Guardar archivos del proyecto fuera de `E:\APP-INVENTARIO\`

### Antes de cualquier cambio de código
```
TOCO:        [función exacta]
ARCHIVO:     [app.js | index.html | style.css]
RAZÓN:       [una línea]
NO TOCO:     [qué queda igual y por qué]
```

### Al terminar sesión con cambios
1. `ACTUALIZAR_GITHUB_APP_INVENTARIO.bat` para commitear y publicar
2. Guardar estado en `MEMORIA_PROYECTO.md`

---

## ARQUITECTURA RÁPIDA

### Vistas (todas deben tener rama en refreshView)
- `view-2025` / `view-2026` — análisis por año (embudo 30% + drilldown 70%)
- `view-comparative` — comparativo 2025 vs 2026
- `view-final` — análisis final consolidado con filtros
- `view-checklist` — checklist de inventario (estático)
- `view-mejoras` — sugerencias de mejora (acordeones, estático)
- `view-reconteo` — centro de reconteo operacional
- `view-2025v2` — análisis avanzado 2025
- `view-planos` — planos de patentes (estático)

### Funciones de datos filtrados
- `getFilteredData(year)` → 2025 / 2026
- `getFilteredDataComp()` → { d25, d26 }
- `getFilteredDataFinal()` → Análisis Final

### Regla PLANO_SHEETS (CRÍTICA)
`const PLANO_SHEETS` vive justo antes de `function renderPlanos()`. Nunca debe eliminarse.
Si desaparece → `ReferenceError` → todos los tabs del nav quedan sin handler.

---

## HERRAMIENTAS PORTABLES

```
Node.js:  E:\nodejs-portable\node.exe
Git:      E:\git-portable\mingw64\bin\git.exe
```

---

## Registro de corridas (16-10-2026)
- `ACTUALIZAR_GITHUB_APP_INVENTARIO.bat` enganchado al registro de corridas del Centro de Control (encabezado de 7 lineas, proyecto `appinventario`); queda en el calendario con su log. El .bat paso a fin de linea CRLF (obligatorio: con solo LF los goto/etiquetas fallan). Respaldo: E:\_ARCHIVO_FERRETERIA\appinventario-bat-respaldo-20261016. Sin commit ni push hechos.
