# Cómo convertir los `.md` a PDF (para todo el equipo)

Guía para exportar los documentos del peritaje de **Markdown (.md) → PDF** con VS Code.
Cada integrante entrega de forma individual, así que cada quien genera sus PDF (o uno los
genera y los comparte).

---

## Paso 1 — Instalar la extensión (una sola vez)
1. Abre **VS Code** en la carpeta del proyecto.
2. Panel de **Extensiones**: `Ctrl + Shift + X`.
3. Busca **`Markdown PDF`** (autor **yzane**, icono morado) → **Install**.

## Paso 2 — Apuntar la extensión a un navegador (¡importante!)
La extensión usa un navegador Chromium para renderizar. Si no se configura, da el error
*"Failed to launch the browser process"*. Solución:
1. Abre Configuración: `Ctrl + ,`.
2. Busca: **`markdown-pdf.executablePath`**.
3. Pega la ruta de **Microsoft Edge** (existe por defecto en Windows):
   ```
   C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
   ```
   > Si tu Edge está en otra ruta o usas Chrome, usa la ruta de tu navegador. Para Chrome suele ser
   > `C:\Program Files\Google\Chrome\Application\chrome.exe`.
4. **Reinicia VS Code** (cierra y vuelve a abrir).

## Paso 3 — Exportar cada documento
Por cada archivo: ábrelo, **clic derecho** dentro del texto → **`Markdown PDF: Export (pdf)`**.
El PDF se genera en la **misma carpeta** que el `.md`.

### Documentos a exportar (en este orden de prioridad)
| # | Archivo `.md` | PDF resultante |
|---|---|---|
| 1 | `06_INFORME_FINAL/informe_pericial.md` | **informe_pericial.pdf** ← el principal |
| 2 | `01_IDENTIFICACION/informe_preliminar.md` | informe_preliminar.pdf |
| 3 | `BITACORA_PERICIAL.md` | bitacora_pericial.pdf |
| 4 | `05_CUSTODIA/registro_cadena_custodia.md` | registro_cadena_custodia.pdf |
| 5 (opcional) | `CHECKLIST_ENTREGA.md`, `PLAN_MAESTRO.md`, `README.md` | — |

## Plan B — Si el Export (pdf) falla
1. Clic derecho → **`Markdown PDF: Export (html)`** (genera un `.html`).
2. Abre ese `.html` en **Edge/Chrome** → `Ctrl + P` → Destino **"Guardar como PDF"** → Guardar.
   > Este método nunca falla porque no depende del Chromium interno de la extensión.

## Notas
- Las **tablas** y los símbolos ✅/⚠️ se renderizan bien en el PDF.
- El informe **no** incrusta imágenes (solo referencia rutas), así que no habrá imágenes rotas.
- Antes de entregar: en el **informe**, llenar la **tabla de firmas (§12)** y adjuntar la
  constancia de idoneidad de cada perito.
- Los PDF **sí** son parte del entregable y se pueden subir al repo (no están en `.gitignore`).
