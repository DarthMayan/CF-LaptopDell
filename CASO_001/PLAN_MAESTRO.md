# Plan Maestro del Peritaje — Caso 24042024-001-Pavana-Hidalgo

Documento de control interno (no es entregable). Define fases, orden de trabajo,
mapa de objetivos→evidencia→herramienta y el estado de avance.

## Principio metodológico (orden de fases)

Se sigue el flujo **NIST SP 800-86 / ISO/IEC 27037**: **Identificación → Preservación →
Recolección → Análisis → Reporte**. No se analiza nada antes de preservar y verificar
integridad. Todo se hace sobre **copias de trabajo**; los originales son de solo lectura.

## Fases y estado — **ANÁLISIS COMPLETO**

| Fase | Descripción | Carpeta | Estado |
|---|---|---|---|
| 0 | Estructura + bitácora + plan | `/CASO_001/` | ✅ Hecho |
| 1 | **Preservación: integridad/hashing** de todos los indicios | `02_PRESERVACION/hashes/` | ✅ Hecho (E01 Match + 9/9 PASS) |
| 2 | Identificación (equipo, SO, disco, instalador) | `01_IDENTIFICACION/` | ✅ Hecho |
| 3 | Análisis de memoria (Volatility) | `02_PRESERVACION/{memoria,procesos,red}/` | ✅ Hecho |
| 4 | Análisis de registro (hives de triage) | `03_ANALISIS/` | ✅ Hecho |
| 5 | Análisis de disco E01 (Autopsy) | `03_ANALISIS/` | ✅ Hecho |
| 6 | Credenciales y DPAPI | `03_ANALISIS/correlacion/` | ✅ Hecho (contraseña `MyPassword` + DPAPI) |
| 7 | Timeline 20–24 abr 2024 + correlación | `03_ANALISIS/timeline/` | ✅ Hecho |
| 8 | Redacción informe final | `06_INFORME_FINAL/` | ✅ Redactado (pendiente PDF + firmas) |

> **Estado global:** los 12 objetivos y las profundizaciones (contraseña, DPAPI, archivos cifrados,
> usuarios ocultos, 2º SID = imagen maestra) están **cerrados**. Solo resta exportar a PDF y firmar.

## Mapa objetivo → evidencia → herramienta

| Obj | Qué pide | Fuente principal | Herramienta |
|---|---|---|---|
| 1 | Marca/modelo/serie equipo + SO | hive SYSTEM, SOFTWARE | Volatility 3 + Autopsy + regipy |
| 2 | Disco: geometría, serie | Cadena custodia + .E01 | FTK Imager + Autopsy |
| 3 | ¿Actividad post-adquisición? | LNK/timestamps vs adquisición | Autopsy |
| 4 | Quién instaló SO/apps | SOFTWARE (RegisteredOwner/InstallDate), SAM | regipy + Autopsy |
| 5 | Timeline 20–24 abr 2024 | BAM, web, LNK, USB | Autopsy |
| 6 | Credenciales / cifrado | SAM+SYSTEM, DPAPI de ken | extractor propio (regipy+pycryptodome) + dpapick3 + rockyou |
| 7 | Actividad de red | memdump (netscan), navegador | Volatility 3 + Autopsy |
| 8 | Herramientas/artefactos | Installed/Run Programs, procesos RAM | Volatility 3 + Autopsy |
| 9 | Integridad / hashing | todos los indicios | FTK Imager + hashlib |
| 10 | ¿Seguimiento a personas? | web (OSINT/Censys/Shodan), descargas | Autopsy + Volatility |
| 11 | ¿Exfiltración? | netscan, USB, FTP/P2P/nube | Volatility + Autopsy |
| 12 | Inconsistencias | comparación documental + registro | análisis manual + regipy |

## Nota histórica (orden de ejecución seguido)

El trabajo inició por la **Fase 1 (Preservación / integridad)** —primer paso metodológico
obligatorio y 25% de la evaluación— y continuó por memoria, registro y disco, cerrando con
credenciales/DPAPI, timeline y redacción. La secuencia y cada paso quedan registrados en
`BITACORA_PERICIAL.md` (32 actividades). Estado de cierre en `CHECKLIST_ENTREGA.md`.
