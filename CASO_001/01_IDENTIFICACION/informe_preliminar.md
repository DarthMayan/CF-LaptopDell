# Informe Preliminar de Identificación
### Caso 24042024-001-Pavana-Hidalgo · Fase 1 (Identificación)

> Documento de la **fase de identificación** (NIST SP 800-86 / ISO/IEC 27037). Registra la
> recepción, el inventario y la identificación inicial de los indicios, previo al análisis a
> fondo (que se desarrolla en `06_INFORME_FINAL/informe_pericial.md`).
> *Se exportará a `informe_preliminar.docx`/PDF para la entrega.*

- **Equipo pericial (peritos terceros designados):**
  - Diego Morales Gómez — 0250015@up.edu.mx
  - Ramón Andrés Galindo Gerardo — 0248040@up.edu.mx
  - Luis Atristain Alfaro — 0246760@up.edu.mx
  - Montserrat Castillo Vega — 0255627@up.edu.mx
  - Fernando Mauricio Chavarría Reyes — 0253214@up.edu.mx
  - Cecilia Gaona Vidales — 0267688@up.edu.mx
  - José Gabriel Hernández Castresana — 0253264@up.edu.mx
- **Entidad solicitante:** Fiscalía General del Estado — Dirección de Peritos y Ciencias Forenses
- **Fecha:** 2 de junio de 2026
- **Equipo de análisis:** MAYAN (Windows 11), software libre/licenciado documentado en metodología.

---

## 1. Objeto
Documentar de manera preliminar los indicios recibidos, verificar su integridad e identificar el
equipo de cómputo y los soportes asociados, como base para el análisis pericial.

## 2. Indicios recibidos (inventario)

| Indicio | Tipo | Archivo / detalle | Tamaño |
|---|---|---|---|
| 001 | Memoria volátil | `Dump memoria/memdump.mem` | 9.0 GB (RAM física 8 GB) |
| 002 | Triage de registro | `Triage/` — SAM, SECURITY, SYSTEM, SOFTWARE, DEFAULT, NTUSER/UsrClass (ken, Default) + claves DPAPI | ~96 MB |
| 003 | Imagen de disco | `Imagen de disco/001-003-LAptop-Pavana T3.E01` (EnCase E01) | ~465 GiB lógicos |
| Doc. | Cadena de custodia | `24042024_001-003-Pavana-Hidalgo-RCDC.pdf` | — |
| Doc. | Solicitud pericial | `Solicitud Pericial.pdf` | — |

## 3. Identificación del equipo y soportes

| Elemento | Valor |
|---|---|
| Nombre del equipo (hostname) | **DESKTOP-2TQHS9Q** |
| Sistema operativo | **Windows 10 Pro 22H2** (build 19045), x64 |
| Titular registrado / usuario | **ken** (SID …-1001) |
| Fecha de instalación del SO | **2024-04-21** (UTC−6) |
| Disco origen (custodia) | Seagate **ST950042 0AS**, S/N **5VJ8Z5ZN** |
| Geometría | 976,773,152 sectores × 512 B (~500 GB); partición principal NTFS ~465 GiB |

## 4. Verificación de integridad (resumen)
- **Imagen E01:** MD5 `6ace19abd1a8d25589be07d68e9a7bcc` / SHA-1 `3b401352…` → **Match** (FTK Imager), sin bad blocks.
- **Memoria + 8 hives:** **9/9 PASS** (MD5/SHA-1/SHA-256) contra los valores documentados.
- Detalle en `02_PRESERVACION/hashes/reporte_integridad.md` y capturas en `04_EVIDENCIA/capturas/`.

## 5. Cadena de custodia
Referencia: `05_CUSTODIA/` (copia del RCDC + registro de continuidad). Los indicios se reciben
para análisis; se trabaja sobre **copias** con los originales en **solo lectura**.

## 6. Observaciones preliminares
Se detectan inconsistencias documentales en la cadena de custodia (fechas, hashes de copia en
blanco) que se detallan en el informe final (§7.12, objetivo 12).

## 7. Conclusión preliminar y siguiente fase
Los indicios son **íntegros y aptos para análisis**. Se procede a las fases de análisis de memoria
(Volatility), registro y disco (Autopsy), cuyos resultados se consignan en el **informe pericial
final** (`06_INFORME_FINAL/`).
