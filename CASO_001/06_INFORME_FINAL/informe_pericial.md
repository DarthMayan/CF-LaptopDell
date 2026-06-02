# INFORME PERICIAL EN INFORMÁTICA FORENSE
### Caso 24042024-001-Pavana-Hidalgo

> **Documento de trabajo (borrador).** Se redacta en Markdown y se exportará a
> **PDF** para la entrega final (requisito). Las secciones se completan conforme
> avanza el análisis; lo marcado con _[pendiente]_ se llena con hallazgos verificados.

---

## Portada
- **Título:** Informe Pericial en Informática Forense — Análisis de imagen forense de equipo de cómputo
- **Número de caso:** 24042024-001-Pavana-Hidalgo
- **Entidad solicitante:** Fiscalía General del Estado — Dirección de Peritos y Ciencias Forenses
- **Fiscal:** Lic. Alessandro Tapia Ochoa
- **Perito:** Diego Morales Gómez — 0250015@up.edu.mx
- **Fecha de emisión:** _[pendiente]_
- _(Imagen corporativa / logo)_

---

## 1. Resumen Ejecutivo
_[pendiente — síntesis de hallazgos, propósito y conclusiones principales, en lenguaje accesible]_

---

## 2. Introducción
- **Contexto del caso:** _[pendiente]_
- **Objetivos del peritaje:** ver §5.
- **Consideraciones para evitar sesgos:** análisis basado solo en evidencia verificable; hipótesis falsables; cadena de custodia documentada; trabajo sobre copias.

---

## 3. Metodología
- **Marco:** NIST SP 800-86; ISO/IEC 27037 (adquisición/preservación), 27041 (metodología), 27042 (análisis e interpretación); Guía del Primer Respondiente (INTERPOL); SWGDE.
- **Fases:** Identificación → Preservación → Recolección → Análisis → Reporte.
- **Herramientas (con versión):** FTK Imager _[ver]_, Volatility 3 _[ver]_, Autopsy _[ver]_, RegRipper _[ver]_, Python 3.13.6, impacket _[ver]_. _(registrar versión exacta de cada una)_
- **Preservación:** verificación por hashing (MD5/SHA-1/SHA-256); originales en solo lectura; trabajo sobre copias.

---

## 4. Descripción de los Indicios
| Indicio | Tipo | Detalle | Estado recepción |
|---|---|---|---|
| 001 | Memoria volátil | `memdump.mem`, 9.0 GB, RAM 8 GB | Íntegro _[verificar]_ |
| 003 | Imagen de disco | `001-003-LAptop-Pavana T3.E01`, EnCase E01, ~40 GB | Íntegro _[verificar]_ |
| — | Hives de registro | SAM, SECURITY, SYSTEM, SOFTWARE, DEFAULT, NTUSER/UsrClass (ken, Default) | Íntegro _[verificar]_ |
| — | Disco origen | Seagate ST950042 0AS, S/N 5VJ8Z5ZN | Documental |

---

## 5. Planteamiento del Problema (objetivos íntegros)
1. Marca, modelo, número de serie del equipo y del sistema operativo.
2. Marca, modelo, serie y geometría física del/los disco(s).
3. ¿Existió actividad posterior a la obtención de los indicios?
4. Usuario/entidad que instaló el SO y aplicaciones principales.
5. Trazar las actividades del equipo entre el 20 y el 24 de abril de 2024.
6. Recuperar credenciales de acceso y/o documentos cifrados (documentar técnicas).
7. Reconstruir la actividad de red (entrante y saliente) en el periodo de interés.
8. Identificar herramientas/artefactos de software (administración, borrado, exfiltración, monitoreo).
9. Verificar y certificar la integridad de los elementos probatorios (método y norma).
10. Determinar si el equipo se usó para seguimiento de personas (fuentes, herramientas, evidencias).
11. Demostrar si se extrajo/transmitió información (vectores y mecanismos).
12. Señalar inconsistencias en los indicios (NIST, ENFSI, SWGDE + normativa mexicana).

---

## 6. Hipótesis
- **General:** _[pendiente — formular de forma falsable]_
- **De apoyo:** _[pendiente]_

---

## 7. Análisis Técnico
_(Explicación paso a paso, con glosario, capturas, tablas y referencias cruzadas a la bitácora.)_

### 7.1 Integridad de la evidencia (obj. 9)  _[en curso — Fase 1]_
### 7.2 Identificación de equipo y SO (obj. 1)  _[pendiente]_
### 7.3 Disco: geometría y serie (obj. 2)  _[pendiente]_
### 7.4 Instalación del SO / titular (obj. 4)  _[pendiente]_
### 7.5 Actividad posterior a la adquisición (obj. 3)  _[pendiente]_
### 7.6 Línea de tiempo 20–24 abr 2024 (obj. 5)  _[pendiente]_
### 7.7 Credenciales y cifrado / DPAPI (obj. 6)  _[pendiente]_
### 7.8 Actividad de red (obj. 7)  _[pendiente]_
### 7.9 Herramientas y artefactos de software (obj. 8)  _[pendiente]_
### 7.10 Seguimiento a personas (obj. 10)  _[pendiente]_
### 7.11 Exfiltración / transmisión de información (obj. 11)  _[pendiente]_
### 7.12 Inconsistencias en los indicios (obj. 12)  _[material preliminar en bitácora]_

---

## 8. Hallazgos Clave
_[pendiente — evidencia relevante y su relación con cada hipótesis]_

---

## 9. Conclusiones
_[pendiente — interpretación objetiva, simétrica con las hipótesis, con limitaciones del análisis]_

---

## 10. Recomendaciones (opcional)
_[pendiente]_

---

## 11. Anexos
- A. Reporte de hashes (`02_PRESERVACION/hashes/reporte_integridad.md`).
- B. Salidas de Volatility (`02_PRESERVACION/`).
- C. Capturas (`04_EVIDENCIA/capturas/`).
- D. Bitácora pericial completa (`BITACORA_PERICIAL.md`).
- E. Cadena de custodia (`05_CUSTODIA/`).

---

## 12. Firma y Credenciales
- **Perito:** Diego Morales Gómez
- **Correo:** 0250015@up.edu.mx
- **Firma electrónica avanzada:** _[pendiente]_
- **Constancia de idoneidad profesional:** _[pendiente]_

---

## Referencias normativas y científicas
- Guía del Primer Respondiente — INTERPOL.
- NIST SP 800-86 — *Guide to Integrating Forensic Techniques into Incident Response*.
- ISO/IEC 27037:2012; ISO/IEC 27041; ISO/IEC 27042.
- Código Nacional de Procedimientos Penales (México).
- Ley Federal de Protección de Datos Personales en Posesión de los Particulares.
- _[≥2 papers/artículos científicos — pendientes de seleccionar]_
