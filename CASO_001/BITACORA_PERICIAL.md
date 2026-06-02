# Bitácora Pericial — Caso 24042024-001-Pavana-Hidalgo

> Registro cronológico de todas las actividades del peritaje. Cada entrada documenta
> qué se hizo, con qué herramienta/versión, sobre qué evidencia, el resultado y el
> responsable. Sustenta los criterios de **Preservación (25%)** y **Documentación (15%)**
> y la reproducibilidad exigida (ISO/IEC 27037 §7, ISO/IEC 27041).
>
> **Regla de oro:** ninguna acción sobre la evidencia sin registrarla aquí. No se
> manipula evidencia sin documentar (req. de entrega). Trabajar siempre sobre copias;
> los originales (.E01, .mem) son de solo lectura.

**Perito:** Diego Morales Gómez — 0250015@up.edu.mx
**Equipo de trabajo:** MAYAN (Windows 11 Home SL 10.0.26200)
**Zona horaria de referencia:** UTC−6 (Centro de México) — declarar siempre el huso al reportar timestamps.

---

## Registro de actividades

| # | Fecha/Hora (UTC−6) | Actividad | Herramienta (versión) | Evidencia | Resultado | Responsable |
|---|---|---|---|---|---|---|
| 001 | 2026-06-02 | Recepción y reconocimiento de indicios; inventario de la carpeta `Laptop Dell/` | Inspección manual | Todos | Inventario completo (2 PDF, 2 hashes .txt, .mem 9GB, .E01 40GB, hives triage) | Diego |
| 002 | 2026-06-02 | Creación de estructura de trabajo `/CASO_001/` y bitácora | — | — | Estructura de 6 carpetas creada | Diego |
| 003 | 2026-06-02 16:45 | Verificación de integridad (hashing MD5/SHA-1/SHA-256) de memoria volátil y 8 hives de registro | `verificar_integridad.py` (Python 3.13.6, hashlib) | memdump.mem + SAM/SECURITY/SYSTEM/SOFTWARE/DEFAULT + NTUSER/UsrClass (ken) + NTUSER (Default) | **9/9 PASS** — todos los MD5/SHA-1 coinciden con lo documentado. Reporte: `02_PRESERVACION/hashes/reporte_integridad.md` | Diego |
| 004 | 2026-06-02 16:42→17:45 | Verificación de integridad de la imagen de disco E01 (función nativa Verify) | FTK Imager 4.7.3.81 | `001-003-LAptop-Pavana T3.E01` (976,773,152 sectores) | **MATCH** — MD5 `6ace19abd1a8d25589be07d68e9a7bcc` y SHA-1 `3b401352e1b6b60f73dd30dce97f12c85a2adae7` (computed = stored = report). **Sin bad blocks.** Captura `Captura de pantalla 2026-06-02 174510.png`. **Objetivo 9 cerrado.** | Diego |

| 005 | 2026-06-02 17:09 | Recálculo de hashes en vivo + captura de pantalla como respaldo visual auditable | `capturar_hashes.ps1` (PowerShell, Get-FileHash) | 9 indicios crudos | **9/9 PASS** corroborado visualmente. Evidencia: 2 capturas en `04_EVIDENCIA/capturas/` (ver `INDICE_CAPTURAS.md`) | Diego |
| 006 | 2026-06-02 | Instalación de Volatility 3 para análisis de memoria | `pip install volatility3` → **Volatility 3 Framework 2.28.0** (+ pefile 2024.8.26) | — | Instalado OK; `vol --help` operativo (entry point en PATH) | Diego |
| 007 | 2026-06-02 | Identificación del SO y validación del volcado de memoria | `vol -f $IMG windows.info` (Volatility 3 2.28.0) | memdump.mem | Imagen válida (símbolos kernel cargados). **Windows 10 NT 10.0 build 19041 (v2004), x64, WinNt, 8 CPU.** SystemTime **2024-04-23 16:17:45 UTC = 10:17:45 UTC-6**. Salida: `02_PRESERVACION/memoria/01_info.txt` | Diego |

> A partir de aquí se añade una fila por cada paso ejecutado. Cuando ejecutes un
> comando, pega aquí el comando exacto, la versión de la herramienta y el hash/salida
> relevante. Yo te ayudo a redactar cada entrada conforme avancemos.

> **Nota de herramienta (obj. 12):** el ejecutable de FTK Imager aparece rotulado como
> **"Exttero FTK Imager 4.7.3.81"** en la barra de título (ver captura), versión distinta
> a la declarada en la cadena de custodia/imagen (**AccessData FTK Imager 4.7.2.11**).
> Se documenta como observación: la *verificación* se hace con una build distinta a la de
> *adquisición*; no afecta la integridad (el hash es independiente de la herramienta que lo
> recalcula) pero debe constar.

---

## Hallazgos preliminares (se trasladan al informe)

- **Posibles inconsistencias en la cadena de custodia** (objetivo 12) — pendientes de confirmar:
  - Disco declarado **500 GB / 38,913 cilindros** vs. imagen reporta **~466 GB / 60,801 cilindros** y tipo "USB Device".
  - Fecha de adquisición de memoria volátil en la custodia: **"24-Abril-2014 10:26"**. El año (2014) es erróneo y el día discrepa: la evidencia técnica (Volatility `windows.info` SystemTime = **2024-04-23 10:17 UTC-6** + *Created Time* del `.mem`) sitúa la captura el **23 de abril de 2024 ~10:17**.
  - Campos **"HASH MD5 / SHA-1 copia forense" en blanco** en la cadena de custodia (aunque la integridad sí se verificó: E01 Match y 9/9 hives PASS).
  - Fecha de inicio de adquisición del disco: **15-Abril-2024 11:10** (celda de la custodia) vs **23-Abril-2024 11:10** (encabezado/notas FTK del `.E01`). La hora coincide (11:10); discrepa el día (15 vs 23).
  - Herramienta de verificación: **Exterro FTK Imager 4.7.3.81** vs adquisición **AccessData FTK Imager 4.7.2.11**.
