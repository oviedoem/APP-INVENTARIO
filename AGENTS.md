# AGENTS.md — APP-INVENTARIO · El Manzano
# Instrucciones para Claude (y cualquier agente de IA) al trabajar en este proyecto

---

## REGLA — NO DIAGNOSTICAR SIN CERTEZA (permanente desde V7.9)

Antes de concluir que algo "no es una patente", "es una etiqueta de zona" o cualquier
afirmación sobre la estructura del Excel o los datos:

1. **Verificar primero en el Excel real** — nunca asumir basándose solo en la posición de la celda o el número de dígitos.
2. **Si hay duda → preguntar al usuario** antes de descartar o ignorar el dato.
3. Ejemplo de error documentado: patentes 1-9 en Sala EXHIBICION fueron erróneamente clasificadas como "etiquetas de zona". El Excel y REGISTROS sí tenían esos números como patentes reales con productos contados.

---

## REGLA — REGENERAR PLANOS (permanente desde V7.10)

Al correr `generar_planos.js` y actualizar las 4 funciones `_planoHtml_X()` en `app.js`:

1. **Verificar que `const PLANO_SHEETS` sigue presente** en app.js después del reemplazo.
   - Posición correcta: justo antes de `function renderPlanos()`.
   - Si no aparece en `grep 'const PLANO_SHEETS' app.js` → restaurar inmediatamente.
2. **Por qué:** `PLANO_SHEETS` vive entre `_planoHtml_PATIO_CONSTRUCTOR` y `renderPlanos()`. Un script de reemplazo que use `\nfunction` como delimitador lo borra. Su ausencia es un `ReferenceError` que aborta el DOMContentLoaded → todos los tabs del nav quedan sin handler.

---

## REGLA ANTI-RETROCESO — OBLIGATORIA EN CADA SESIÓN (mejorada V7.22)

### PASO 0 — Declarar antes de editar (siempre)
```
TOCO:     [nombre exacto de la función]
ARCHIVO:  [app.js | index.html | style.css]
RAZÓN:    [una línea — qué cambia y por qué]
NO TOCO:  [funciones adyacentes que NO se tocan]
```

### PASO 1 — Checklists según tipo de cambio

**Si agregas una clave a `state.*` (p.ej. `state.filters.final`):**
```
□ Grep: state.filters = {   → actualizar TODOS los literales de inicialización
□ clearSavedSession()        → incluir la nueva clave en el reset
□ loadStateFromLS()          → agregar guardia post-merge para compatibilidad con snapshots viejos
□ clearFilters(mode)         → incluir la nueva clave en el reset por modo
□ updateFilterBadge(mode)    → verificar que lee la nueva clave correctamente
□ Nueva función que LA LEE   → usar || {} o || '' (nunca acceso directo sin guard)
```

**Si agregas un nuevo modo/vista (p.ej. mode='final'):**
```
□ refreshView()              → agregar rama explícita else if (mode === 'final')
□ clearFilters(mode)         → verificar que el reset incluye el modo
□ renderFilters(mode)        → agregar los grupos de filtro para ese modo
□ closeFilterPanel(mode)     → ya usa ?. así que es seguro, pero verificar
□ index.html                 → agregar filter-drawer-{mode}, filter-overlay-{mode}, filter-badge-{mode}
□ DOMContentLoaded           → revisar si el tab-btn del modo nuevo necesita handler propio
```

**Si modificas una función de render que usa datos filtrados:**
```
□ Verificar que usa getFilteredData*() y NO state.data2026 directo
□ Si hay botón de exportar en esa vista → también actualizar la función export*()
□ Si hay función de reporte en esa vista → también actualizar generateReport*()
```

**Si modificas `isBlankLike()` o `cleanText()`:**
```
□ Estas funciones afectan TODO el pipeline de lectura de Excel
□ Buscar usos: rowValueByAliases, applyRowMapping, buildFamiliaIndex, buildMissingDataIndex
□ Verificar que valores legítimos no queden capturados como "blank"
```

### PASO 2 — Invariantes que NUNCA deben romperse
```
state.filters[mode]      siempre existe para '2025', '2026', 'comparative', 'final'
                         siempre tiene: marca, familia, perfamilia, subfamilia
state.searchText[mode]   siempre existe para '2025', '2026', 'comparative', 'final'
state.drilldown[year]    siempre existe para '2025' y '2026'
state.compDrill          siempre tiene: { field, value }
refreshView()            maneja explícitamente TODOS los modos: 2025, 2026, final, comparative,
                         reconteo, mejoras, 2025v2, checklist, planos
loadStateFromLS()        después del Object.assign, garantizar TODAS las claves nuevas con guards
```

### PASO 3 — Pre-commit checklist (antes de cada git commit)
```
□ node --check app.js                    → sin errores de sintaxis
□ Bump cache-bust en index.html          → app.js?v=X.XX+1
□ ¿Se tocó state.filters?               → verificar clearSavedSession + loadStateFromLS
□ ¿Se agregó modo nuevo?                → verificar refreshView() tiene rama para él
□ ¿Se cambió renderAnalisisFinal()?     → verificar que refreshView lo llama
□ ¿Se cambió getFilteredData*()?        → verificar guard || {} en todas las funciones que la llaman
□ Abrir browser, recargar, ir a cada tab afectado → sin errores en consola
```

### PASO 4 — Funcionalidades protegidas (NUNCA eliminar)
- Color print: `* { -webkit-print-color-adjust: exact !important }` en @media print
- Excel profesional: `exportTableToExcel` con estilos, bordes, formatos
- Email Final sin auto-print: rama 'final' de `emailReport` sin `printMode` bloqueante
- Reconteo prioridad/clic: `_recountPriority`, `recountFiltrarPorFila`
- Persistencia: `saveDataToIDB`, `loadDataFromIDB`, `restoreSession`
- Planos merges: `renderPlanoGrid` con `spanMap`/`skipSet`
- Planos cobertura: `getPlanoContados`, colores en `patenteStyle`
- Lookup familia: `buildFamiliaIndex` guarda clave exacta + normalizeSku + numStr
- Guard localStorage: `loadStateFromLS` garantiza `filters.final`, `searchText.final`,
  `filters.comparative.subfamilia` después del Object.assign

**Señal de alerta:** Un cambio que necesita tocar más de 2 funciones → analizar impacto completo ANTES de editar la primera.

---

## REGLA DE CIERRE DE SESIÓN — PUSH PENDIENTE

Antes de terminar cualquier sesión donde se hayan modificado archivos en `E:\APP-INVENTARIO\`, Claude DEBE:

1. Ejecutar `git status` en `E:\APP-INVENTARIO\`
2. Si hay archivos modificados o sin commitear → hacer `git add -A && git commit && git push`
3. Verificar que GitHub Pages se republica (el workflow se dispara automáticamente en cada push)
4. Nunca dejar `app.js`, `index.html`, `style.css` o `planos_generated.js` modificados sin publicar

Patrón de riesgo: se edita el código, se prueba localmente, la sesión termina con otras tareas → el push final se olvida y GitHub Pages queda desactualizado.

Comando rápido:
```
cd E:\APP-INVENTARIO && git add -A && git status
```
Si hay cambios → commitear con mensaje descriptivo y hacer push.

---

## PROYECTO INDEPENDIENTE — REGLA ABSOLUTA

```
TRABAJAR SOLO EN:   E:\APP-INVENTARIO\
NUNCA TOCAR:        Cualquier archivo fuera de E:\APP-INVENTARIO\
                    En particular E:\ferreteria-oviedo\ es OTRO proyecto (panel-admin,
                    panel-cliente, panel-vendedor, pipeline ERP). No mezclar.

REPO GITHUB:        https://github.com/oviedoem/APP-INVENTARIO  (público)
DEPLOY ONLINE:      https://oviedoem.github.io/APP-INVENTARIO/  (GitHub Pages, auto en cada push)

PERSISTENCIA (FIX V7.13):
  El init en DOMContentLoaded LLAMA a restoreSession() (no la anula como antes).
  Si hay datos guardados → banner #session-restore-banner los restaura.
  Si no → app arranca limpia y muestra welcome.
  Para forzar limpieza: botón 🧹 Limpiar del header (clearAllApp) o "Empezar de cero" en el banner.
  IndexedDB y localStorage son por dispositivo — NO hay sync entre PC y celular.
```

Este proyecto NO forma parte del panel admin/cliente/vendedor de Ferretería Oviedo.
Es una SPA independiente. No compartir código, no abrir previews de otros proyectos,
no leer archivos fuera de esta carpeta.

---

## ARCHIVOS DEL PROYECTO

```
E:\APP-INVENTARIO\
  index.html            — estructura HTML + vistas
  style.css             — estilos (CSS variables + componentes)
  app.js                — lógica completa (state, parseo, render, filtros)
  MEMORIA_PROYECTO.md   — documentación técnica y estado actual
  AGENTS.md             — este archivo
  datos/                — archivos de datos (NO editar)
  .claude/              — configuración local del entorno
```

---

## ANTES DE CUALQUIER CAMBIO

### 1. Leer MEMORIA_PROYECTO.md

Contiene el estado actual del proyecto, funciones JS, clases CSS y historial.
Es la fuente de verdad — leerla antes de proponer cualquier cambio.

### 2. Declarar alcance (Safe Change)

Para cualquier modificación en `app.js`:

```
TOCO:     [nombre exacto de la función]
ARCHIVO:  app.js
RAZÓN:    [una línea — qué se cambia y por qué]
NO TOCO:  [funciones adyacentes que NO se van a modificar]
```

**Un prompt = una función.** Si se necesitan dos funciones → dos prompts en orden.

### 3. Verificar dependencias en app.js

| Si tocas... | Verifica también... |
|---|---|
| `state.filters` (agregar clave) | `clearSavedSession`, `loadStateFromLS` (guard post-merge), `clearFilters`, `updateFilterBadge` |
| `refreshView()` | Que tenga rama explícita para TODOS los modos: 2025, 2026, final, comparative, reconteo, mejoras, 2025v2 |
| `getFilteredData(year)` | Que siga combinando `state.drilldown` + `state.filters` + `searchText` |
| `getFilteredDataFinal()` | Que use `state.filters.final \|\| {}` (guard) |
| `renderAnalisisFinal()` | Que use `getFilteredDataFinal()` (no `state.data2026` directo), que llame `renderFilters('final')` |
| `renderFilters(mode)` | Que modos year/final tengan marca/familia/hiperfamilia/subfamilia + ubicación |
| `clearFilters(mode)` | Que incluya `subfamilia:''`, `final:{}` en el reset, que llame `closeFilterPanel` + `updateFilterBadge` |
| `renderEmbudo(year)` | Que no pise los filtros del drawer |
| `toggleAcc(btn)` | Que `initAccordions()` siga conectando `.acc-btn` al DOMContentLoaded |
| `renderModeComp()` | Que `setCompCategoria()` la llame (no `renderCompCategoria` directo) |
| `buildFamiliaIndex()` | Que guarde clave exacta + normalizeSku + numStr por cada código |
| `isBlankLike()` | Que 'Sin clasificar' siga en la lista; verificar que no capture valores legítimos |
| Cualquier `render*()` | Que los IDs de elementos coincidan exactamente con los del index.html |
| Cualquier `export*()` | Que use datos filtrados (getFiltered*) no datos crudos (state.data*) |

### 4. No romper estos invariantes

```
state.filters[mode]       siempre existe para: '2025', '2026', 'comparative', 'final'
                           claves obligatorias: marca, familia, perfamilia, subfamilia
                           + para year modes: zona, area, patente, bodega
state.searchText[mode]    siempre existe para: '2025', '2026', 'comparative', 'final'
state.drilldown[year]     siempre existe para '2025' y '2026'
state.compDrill           siempre tiene: { field, value } (null cuando inactivo)
refreshView()             DEBE tener rama para CADA modo que existe en el nav
loadStateFromLS()         DESPUÉS del Object.assign, DEBE tener guards para:
                             state.filters.final, state.searchText.final,
                             state.filters.comparative.subfamilia,
                             state.filters['2025'].subfamilia, state.filters['2026'].subfamilia
initAccordions()          debe correr en DOMContentLoaded
updateFilterBadge(mode)   debe llamarse después de cualquier cambio a filters o drilldown
```

---

## CIERRE DE SESIÓN — OBLIGATORIO

Antes de terminar cualquier sesión con cambios:

1. Actualizar `MEMORIA_PROYECTO.md`:
   - Sección **HISTORIAL DE CAMBIOS** con lo que se modificó
   - Sección **PENDIENTE** si quedan tareas abiertas

2. Ejecutar sync a GitHub:
   ```
   E:\APP-INVENTARIO\ACTUALIZAR_GITHUB_APP_INVENTARIO.bat
   ```

3. Confirmar que el commit fue exitoso (aparece hash y "subido a GitHub").

**Nunca cerrar sesión con cambios sin pushear.**

---

## STACK Y RESTRICCIONES

- HTML + CSS + **Vanilla JS** — sin frameworks, sin npm, sin build step
- Las librerías se cargan desde CDN en `index.html` (no agregar nuevas sin pedirlo)
- No agregar dependencias externas
- No crear archivos fuera de `E:\APP-INVENTARIO\`

### CDN activos
```
SheetJS  xlsx-0.20.3     — parseo .xlsx / .xls
PapaParse 5.4.1          — parseo .csv
Chart.js  4.4.3          — gráficos
```

---

## ARQUITECTURA RÁPIDA

### Vistas HTML (todas deben tener rama en refreshView)
```
view-2025         — análisis 2025 (embudo 30% | drilldown+charts 70%)    → renderMode('2025')
view-2026         — análisis 2026 (misma estructura)                      → renderMode('2026')
view-comparative  — comparativo 2025 vs 2026                              → renderModeComp()
view-final        — análisis final consolidado con filtros                → renderAnalisisFinal()
view-checklist    — checklist de inventario                               → no refreshView (estático)
view-mejoras      — sugerencias de mejora (acordeones)                    → no refreshView (estático)
view-reconteo     — centro de reconteo operacional                        → solo muestra la vista
view-2025v2       — análisis avanzado 2025                                → solo muestra la vista
view-planos       — planos de patentes                                    → no refreshView (estático)
```

### Sistema de filtrado (3 capas — V7.20+)
```
Capa 1 — Embudo (state.drilldown):           hiperfamilia → familia → marca   [solo 2025/2026]
Capa 2 — Drawer chips (state.filters):        marca · familia · hiperfamilia · subfamilia
                                              + zona · área · patente · bodega [solo year modes]
Capa 3 — Búsqueda texto (state.searchText):   código o descripción [todos los modos]

Funciones de datos filtrados:
  getFilteredData(year)     → 2025 / 2026 (drilldown + filters + searchText)
  getFilteredDataComp()     → { d25, d26 } para comparativo
  getFilteredDataFinal()    → Análisis Final (filters.final + searchText.final)
```

### Acordeones
```
.mej-acc-header + .mej-acc-body   — acordeones en vista mejoras (onclick inline)
.acc-btn + .acc-content            — acordeones genéricos (conectados por initAccordions)
toggleAcc(btn)                     — función única para ambos tipos
```
