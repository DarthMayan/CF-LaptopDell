# Registro de Continuidad de la Cadena de Custodia
### Caso 24042024-001-Pavana-Hidalgo

> Complementa el documento oficial **`24042024_001-003-Pavana-Hidalgo-RCDC.pdf`** (incluido en
> esta carpeta). Documenta la recepción de los indicios por el perito tercero, la verificación de
> integridad como eslabón de continuidad, y las observaciones detectadas.
> Fundamento: ISO/IEC 27037 (preservación) y **CNPP arts. 227–228** (cadena de custodia).
> *Se exportará a `cadena_custodia.xlsx`/PDF para la entrega si así se requiere.*

## 1. Documento oficial de custodia (resumen)

| Campo | Valor |
|---|---|
| Caso / Evidencias | 001 / 001, 002 y 003 |
| Sitio | Av. Miguel Cervantes Saavedra |
| Disco origen | Seagate ST950042 0AS, S/N 5VJ8Z5ZN |
| Copia forense | `001-003-LAptop-Pavana T3.E01` (FTK Imager + Tableau ForensicBridge) |
| MD5 disco origen | 6ace19abd1a8d25589be07d68e9a7bcc |
| SHA-1 disco origen | 3b401352e1b6b60f73dd30dce97f12c85a2adae7 |
| Unidad destino | USB Toshiba S/N 20220817001348F |

## 2. Recepción por el perito (continuidad)

| Quién | Acción | Fecha/hora | Estado |
|---|---|---|---|
| Equipo pericial 3º (ver §6) | Recepción de indicios para análisis | 2026-06-02 | Íntegros, sellados digitalmente por hash |
| — | Trabajo sobre **copias**; originales en **solo lectura** | — | Sin alteración |

## 3. Verificación de integridad (eslabón de continuidad)

| Indicio | Método | Resultado |
|---|---|---|
| Imagen E01 | FTK Imager 4.7.3.81 — *Verify Drive/Image* | **MATCH** (MD5/SHA-1), sin bad blocks |
| Memoria + 8 hives | Hashing MD5/SHA-1/SHA-256 (Python) | **9/9 PASS** |

> Evidencia: `02_PRESERVACION/hashes/reporte_integridad.md` y capturas en `04_EVIDENCIA/capturas/`.

## 4. Observaciones / inconsistencias documentales (obj. 12)
1. Disco declarado 500 GB / 38,913 cilindros vs. imagen ~465 GiB / 60,801 cilindros.
2. Fecha de adquisición de memoria en custodia: "24-Abril-**2014** 10:26" (año erróneo; real 23-abr-2024).
3. Fecha de adquisición de disco: 15-Abril-2024 (custodia) vs. 23-Abril-2024 (FTK/.E01).
4. Campos **MD5/SHA-1 de la copia forense en blanco** en el formato (la integridad sí se verificó).
5. Herramienta de verificación (Exterro FTK 4.7.3.81) distinta a la de adquisición (AccessData FTK 4.7.2.11).
6. **Actividad peri-adquisición** registrada en la imagen (carpeta del caso navegada en vivo 23-abr 10:12–10:13).

> Estas observaciones **no afectan la integridad técnica verificada** de las copias, pero se
> consignan para su valoración procesal.

## 5. Trazabilidad de copias y hashes
Todos los indicios analizados quedan referenciados por su hash en `reporte_integridad.md`
(Anexo A del informe final), garantizando que lo analizado es idéntico a lo recibido.

## 6. Equipo pericial (peritos terceros designados)
- Diego Morales Gómez — 0250015@up.edu.mx
- Ramón Andrés Galindo Gerardo — 0248040@up.edu.mx
- Luis Atristain Alfaro — 0246760@up.edu.mx
- Montserrat Castillo Vega — 0255627@up.edu.mx
- Fernando Mauricio Chavarría Reyes — 0253214@up.edu.mx
- Cecilia Gaona Vidales — 0267688@up.edu.mx
- José Gabriel Hernández Castresana — 0253264@up.edu.mx
