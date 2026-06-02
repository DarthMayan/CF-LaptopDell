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
| 003 | _pendiente_ | Verificación de integridad (hashing) de los indicios | _por registrar_ | .mem, hives | _por registrar_ | Diego |

> A partir de aquí se añade una fila por cada paso ejecutado. Cuando ejecutes un
> comando, pega aquí el comando exacto, la versión de la herramienta y el hash/salida
> relevante. Yo te ayudo a redactar cada entrada conforme avancemos.

---

## Hallazgos preliminares (se trasladan al informe)

- **Posibles inconsistencias en la cadena de custodia** (objetivo 12) — pendientes de confirmar:
  - Disco declarado **500 GB / 38,913 cilindros** vs. imagen reporta **~466 GB / 60,801 cilindros** y tipo "USB Device".
  - Fecha de adquisición de memoria volátil indica **"2014"** (probable error de captura; el resto del documento es 2024).
  - Campos **"HASH MD5 / SHA-1 copia forense" en blanco** en la cadena de custodia.
  - Fecha de inicio de adquisición del disco: **15-abr** (celda) vs **23-abr** (encabezado FTK / notas).
