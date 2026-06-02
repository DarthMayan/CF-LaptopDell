# Plan Maestro del Peritaje — Caso 24042024-001-Pavana-Hidalgo

Documento de control interno (no es entregable). Define fases, orden de trabajo,
mapa de objetivos→evidencia→herramienta y el estado de avance.

## Principio metodológico (orden de fases)

Se sigue el flujo **NIST SP 800-86 / ISO/IEC 27037**: **Identificación → Preservación →
Recolección → Análisis → Reporte**. No se analiza nada antes de preservar y verificar
integridad. Todo se hace sobre **copias de trabajo**; los originales son de solo lectura.

## Fases y estado

| Fase | Descripción | Carpeta | Estado |
|---|---|---|---|
| 0 | Estructura + bitácora + plan | `/CASO_001/` | ✅ Hecho |
| 1 | **Preservación: integridad/hashing** de todos los indicios | `02_PRESERVACION/hashes/` | ⏳ EN CURSO ← **AQUÍ EMPEZAMOS** |
| 2 | Identificación (equipo, SO, disco, instalador) | `01_IDENTIFICACION/` | ⬜ |
| 3 | Análisis de memoria (Volatility) | `02_PRESERVACION/{memoria,procesos,red}/` | ⬜ |
| 4 | Análisis de registro (hives de triage) | `03_ANALISIS/` | ⬜ |
| 5 | Análisis de disco E01 (FTK/Autopsy) | `03_ANALISIS/` | ⬜ |
| 6 | Credenciales y DPAPI | `03_ANALISIS/correlacion/` | ⬜ |
| 7 | Timeline 20–24 abr 2024 + correlación | `03_ANALISIS/timeline/` | ⬜ |
| 8 | Redacción informe final | `06_INFORME_FINAL/` | ⬜ (esqueleto listo) |

## Mapa objetivo → evidencia → herramienta

| Obj | Qué pide | Fuente principal | Herramienta |
|---|---|---|---|
| 1 | Marca/modelo/serie equipo + SO | hive SYSTEM, SOFTWARE | RegRipper / Autopsy |
| 2 | Disco: geometría, serie | Cadena custodia + .E01 (FTK) | FTK Imager |
| 3 | ¿Actividad post-adquisición? | timestamps vs fecha de adquisición | timeline / hashing |
| 4 | Quién instaló SO/apps | SOFTWARE (RegisteredOwner/InstallDate), SAM | RegRipper |
| 5 | Timeline 20–24 abr 2024 | NTUSER (UserAssist, RecentDocs), $MFT, EVTX | Autopsy / plaso |
| 6 | Credenciales / cifrado | SAM+SYSTEM, DPAPI de ken | secretsdump / dpapi |
| 7 | Actividad de red | memdump (netscan), perfiles red, navegador | Volatility 3 |
| 8 | Herramientas/artefactos | Uninstall, Prefetch, procesos RAM | RegRipper, Volatility, Autopsy |
| 9 | Integridad / hashing | todos los indicios | FTK Imager + hashlib |
| 10 | ¿Seguimiento a personas? | apps, RAM, navegador, archivos | Autopsy / Volatility |
| 11 | ¿Exfiltración? | netscan, USBSTOR, apps cloud | Volatility, RegRipper |
| 12 | Inconsistencias | comparación documental | análisis manual |

## Recomendación de inicio

**Empezar por la Fase 1 (Preservación / integridad)** porque:
1. Es el primer paso correcto metodológicamente — nada se analiza sin verificar integridad.
2. Vale **25%** de la calificación (Preservación).
3. Se puede hacer **ya**, sin instalar nada (Python + FTK Imager que ya tienes).
4. Deja la base documental (hashes certificados) para todo lo demás.

Ver `02_PRESERVACION/hashes/INSTRUCCIONES_HASHING.md` para los pasos.
