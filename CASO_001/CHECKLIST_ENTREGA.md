# Checklist Final de Entrega — Caso 24042024-001-Pavana-Hidalgo

Documento de control para verificar que el entregable cumple **todos** los requisitos del oficio.

## 1. Objetivos del peritaje (12/12) ✅

| # | Objetivo | Estado | Sección informe |
|---|---|---|---|
| 1 | Equipo y SO | ✅ | §7.2 |
| 2 | Disco / geometría | ✅ | §7.3 |
| 3 | Actividad posterior/peri-adquisición | ✅ | §7.5 |
| 4 | Quién instaló SO/apps | ✅ | §7.4 |
| 5 | Timeline 20–24 abr 2024 | ✅ | §7.6 + timeline Autopsy |
| 6 | Credenciales / cifrado | ✅ (hash + **contraseña** + DPAPI) | §7.7 |
| 7 | Actividad de red | ✅ | §7.8 |
| 8 | Herramientas/artefactos | ✅ | §7.9 |
| 9 | Integridad | ✅ | §7.1 |
| 10 | Seguimiento a personas | ✅ | §7.10 |
| 11 | Exfiltración | ✅ | §7.11 |
| 12 | Inconsistencias | ✅ (7) | §7.12 |

> Opcional pendiente: Tarea C (mapear archivos del 2º SID) — requiere terminar el índice de
> Keyword Search; documentada como línea abierta, **no bloquea la entrega**.

## 2. Estructura obligatoria del informe ✅ (contenido)

Portada · Resumen Ejecutivo · Introducción · Metodología · Planteamiento · Descripción de
Indicios · Hipótesis · Análisis Técnico · Hallazgos Clave · Conclusiones · Recomendaciones ·
Anexos · Firma y Credenciales — **todas redactadas**.

## 3. Estructura de carpetas /CASO_001/ ✅ (todas con contenido)

- `01_IDENTIFICACION/` → `informe_preliminar.md`
- `02_PRESERVACION/` → hashes (script, reporte) + salidas de memoria (Volatility)
- `03_ANALISIS/` → `correlacion/` (hashes, password, DPAPI), `autopsy_export/` (CSV), `timeline/` (snapshot)
- `04_EVIDENCIA/capturas/` → integridad + FTK Verify
- `05_CUSTODIA/` → `registro_cadena_custodia.md` + RCDC.pdf
- `06_INFORME_FINAL/` → `informe_pericial.md`
- Control: `PLAN_MAESTRO.md`, `BITACORA_PERICIAL.md` (30 actividades)

## 4. Sustento normativo (20%) ✅
NIST SP 800-86 · ISO/IEC 27037/27041/27042 · INTERPOL · SWGDE/ENFSI · CNPP · LFPDPPP · **2 papers**
(Quick & Choo 2014; Case & Richard 2017).

## 5. Requisitos de entrega
- [ ] **Informe final en PDF** (`informe_pericial.md` → PDF) — *en proceso*
- [ ] PDF del `informe_preliminar.md` (recomendado)
- [ ] PDF de `BITACORA_PERICIAL.md` y `registro_cadena_custodia.md` (recomendado)
- [ ] **Firma electrónica avanzada** de cada perito (tabla de firmas en §12)
- [ ] Constancia de idoneidad de cada perito
- [ ] (Opcional) Logo/imagen corporativa en portada
- [x] Reproducible y verificable (scripts + hashes + bitácora)
- [x] Entrega individual por integrante (cada quien sube su PDF)

## 6. Antes de subir a GitHub
- [x] Evidencia pesada (.mem, .E01, BD de Autopsy, perfiles de navegador) en `.gitignore`
- [ ] Subir los **PDF** generados (sí son parte del entregable)

## 7. Equipo pericial
Diego Morales Gómez · Ramón Andrés Galindo Gerardo · Luis Atristain Alfaro · Montserrat Castillo
Vega · Fernando Mauricio Chavarría Reyes · Cecilia Gaona Vidales · José Gabriel Hernández Castresana.
