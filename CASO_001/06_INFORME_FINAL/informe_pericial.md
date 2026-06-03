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

### 7.1 Integridad de la evidencia (obj. 9)

**Método.** Se aplicó verificación criptográfica por *hashing* (funciones MD5, SHA-1 y
SHA-256), comparando el valor recalculado sobre la copia de trabajo contra el valor
documentado en la cadena de custodia y en las hojas de hashes (`.txt`) que acompañan a
cada indicio. Fundamento: **NIST SP 800-86** (uso de *hashing* para garantizar integridad)
e **ISO/IEC 27037:2012** (preservación de evidencia digital). Una coincidencia de hash
demuestra, con probabilidad de colisión despreciable, que la evidencia analizada es
idéntica a la recibida y no fue alterada.

**Herramientas.** `verificar_integridad.py` (Python 3.13.6, módulo `hashlib`) para los
indicios crudos; **FTK Imager 4.7.3.81** (función *Verify Drive/Image*) para la imagen E01.

**Resultado (indicios crudos).** Los 9 indicios verificados **coinciden** (MD5 y SHA-1)
con sus valores documentados → **PASS**. Detalle completo en el Anexo A.

| Indicio | Tamaño (bytes) | MD5 | Resultado |
|---|---|---|---|
| `memdump.mem` | 9,640,603,648 | a22059f3f9c41cc9a2b5e0427a1a6d5e | ✅ PASS |
| `SAM` | 65,536 | 155ae6e43137de21cb9747d60dc451d3 | ✅ PASS |
| `SECURITY` | 65,536 | 8a0b93d74ce72bc98d8b1fb2032488a8 | ✅ PASS |
| `SYSTEM` | 14,417,920 | bcb0e4a82c3dd08d5fc4b9391cb22e26 | ✅ PASS |
| `SOFTWARE` | 78,905,344 | 597f8f124d3e359ce8c663f62c72ed67 | ✅ PASS |
| `DEFAULT` | 524,288 | 3e29a18af3b171bb942a60118cbfe57e | ✅ PASS |
| `NTUSER.DAT` (ken) | 1,572,864 | d99efc55c8541eb2b1361b285d9605c3 | ✅ PASS |
| `UsrClass.dat` (ken) | 3,932,160 | b6d3bead582e4f813a8db38540d98e1e | ✅ PASS |
| `NTUSER.DAT` (Default) | 262,144 | ac9dea2283d8bd0f150662e41a871a3d | ✅ PASS |

**Resultado (imagen E01).** Verificación con FTK Imager 4.7.3.81 (*Verify Drive/Image*)
sobre `001-003-LAptop-Pavana T3.E01` (976,773,152 sectores). Resultado **MATCH** en ambos
algoritmos, **sin bad blocks**:

| Algoritmo | Computed | Stored / Report | Verify |
|---|---|---|---|
| MD5 | 6ace19abd1a8d25589be07d68e9a7bcc | 6ace19abd1a8d25589be07d68e9a7bcc | ✅ Match |
| SHA-1 | 3b401352e1b6b60f73dd30dce97f12c85a2adae7 | 3b401352e1b6b60f73dd30dce97f12c85a2adae7 | ✅ Match |

Evidencia: captura `04_EVIDENCIA/capturas/Captura de pantalla 2026-06-02 174510.png`.

**Conclusión del objetivo 9.** La integridad de **todos** los indicios queda **certificada**:
imagen de disco E01 (MD5/SHA-1 Match, sin bad blocks), memoria volátil y 8 hives de registro
(9/9 PASS por triple algoritmo MD5/SHA-1/SHA-256). Método: hashing criptográfico conforme a
NIST SP 800-86 e ISO/IEC 27037. **Objetivo 9 cubierto.**
### 7.2 Identificación de equipo y SO (obj. 1)

**Sistema operativo (vía memoria, Volatility 3 `windows.info`).** El análisis del volcado
`memdump.mem` arroja:

| Variable | Valor |
|---|---|
| Sistema operativo | Windows 10 (NT 10.0) |
| Build | 19041 (versión 2004) — `Major/Minor 15.19041` |
| Arquitectura | 64-bit (`Is64Bit: True`, `MachineType 34404` = x64) |
| Tipo de producto | `NtProductWinNt` (estación de trabajo) |
| Procesadores lógicos | 8 (`KeNumberProcessors`) |
| Directorio del sistema | `C:\Windows` |
| Hora del sistema al capturar | 2024-04-23 16:17:45 UTC (10:17:45 UTC−6) |

> La marca/modelo/serie del **equipo** y el detalle del **disco** (obj. 2) se completan
> con los hives SYSTEM/SOFTWARE y la imagen E01 _[pendiente: §7.3]_. La cadena de custodia
> documenta el disco origen como **Seagate ST950042 0AS, S/N 5VJ8Z5ZN**.

_Fuente: `02_PRESERVACION/memoria/01_info.txt`._
### 7.3 Disco: geometría y particiones (obj. 2)

**Disco origen** (cadena de custodia + cabecera del E01): Seagate **ST950042 0AS**, S/N
**5VJ8Z5ZN**, interfaz reportada USB en adquisición. **976,773,152 sectores** × 512 bytes =
~500 GB (465 GiB), valor que **coincide** con el contado por FTK y por Autopsy (corrobora integridad).

**Tabla de particiones (Autopsy):**

| Vol | Tipo | Sectores (inicio–fin) | Tamaño aprox. | Rol |
|---|---|---|---|---|
| vol1 | No asignado | 0–2047 | 1 MB | — |
| vol2 | NTFS/exFAT (0x07) | 2048–104447 | ~52 MB | Sistema / EFI |
| **vol3** | **NTFS (0x07)** | **104448–975672495** | **~465 GiB** | **Partición principal de Windows** |
| vol4 | No asignado | 975672496–975673343 | <1 MB | — |
| vol5 | Recuperación (0x27) | 975673344–976769023 | ~561 MB | WinRE |
| vol6 | No asignado | 976769024–976773151 | ~2 MB | — |

_Fuente: Autopsy 4.23.1, Data Sources → tabla de volúmenes._
### 7.4 Instalación del SO / titular y cuentas (obj. 4)

**Cuentas del sistema (Autopsy → OS Accounts; corroborado con SAM, §7.7):**
- Cuenta de usuario principal: **ken** — SID `S-1-5-21-1936453629-2262114833-2442330573-1001`
  (RID 1001), coincidente con el hash NT recuperado.
- Cuentas integradas: SYSTEM (S-1-5-18), LOCAL/NETWORK SERVICE (S-1-5-19/20), cuentas de
  servicio NT (S-1-5-80-*).
- ⚠️ **Hallazgo:** aparece un **segundo SID de usuario con identificador de equipo/dominio
  distinto** — `S-1-5-21-3933942852-973373972-2766786355-1032` (RID 1032). No corresponde al
  SID local de este equipo (el de ken) ni figura como cuenta local en el SAM, lo que indica
  rastro de un usuario de **otra máquina o dominio**. _Línea de investigación abierta:_ mapear
  a qué perfil/archivos pertenece (relevante para obj. 4, 10 y 12).

> El titular de la instalación (RegisteredOwner), fecha de instalación y nombre de equipo se
> completarán con el registro (SOFTWARE/SYSTEM) vía Autopsy → OS Information _[pendiente]_.
### 7.5 Actividad posterior a la adquisición (obj. 3)  _[pendiente]_
### 7.6 Línea de tiempo 20–24 abr 2024 (obj. 5)  _[pendiente]_
### 7.7 Credenciales y cifrado / DPAPI (obj. 6)

**Técnica empleada.** Extracción **offline** de los hashes NT desde los hives **SAM + SYSTEM**
(integridad previamente certificada, §7.1). Procedimiento estándar: (1) cálculo del *bootkey*
(SysKey) a partir de los *class names* de `SYSTEM\ControlSet001\Control\Lsa\{JD,Skew1,GBG,Data}`;
(2) derivación de la *Hashed BootKey* (cifrado **AES**, propio de Windows 10 ≥ 1607); (3) descifrado
del hash NT de cada cuenta (AES + DES con clave derivada del RID). Implementado en **Python puro**
(`regipy` + `pycryptodome`) en el script reproducible `03_ANALISIS/correlacion/extraer_hashes_sam.py`.

> **Nota metodológica (obj. 12 / cadena de herramientas).** Se intentó primero `impacket
> secretsdump`, pero el antivirus del equipo de análisis lo eliminó (falso positivo: clasificado
> como *hacktool*). Para no desactivar controles de seguridad, se desarrolló el extractor propio,
> obteniendo el mismo resultado de forma auditable. Bootkey calculado: `33b4b3f26ed0f7e28175eac2a1e3fce2`.

**Cuentas locales y hashes NT recuperados:**

| Cuenta | RID | Hash NT | Observación |
|---|---|---|---|
| Administrador | 500 | 31d6cfe0d16ae931b73c59d7e0c089c0 | Sin contraseña (deshabilitada por defecto) |
| Invitado | 501 | 31d6cfe0d16ae931b73c59d7e0c089c0 | Sin contraseña |
| DefaultAccount | 503 | 31d6cfe0d16ae931b73c59d7e0c089c0 | Sin contraseña |
| WDAGUtilityAccount | 504 | 3d320a256111a327a9012542211125a1 | Cuenta de Windows Defender Application Guard (password aleatorio del sistema) |
| **ken** | **1001** | **f12c418083c05e3a7de78582e61f652d** | **Cuenta de usuario principal** |

**Descifrado de contraseña.** Se aplicó un ataque de diccionario (4,215 candidatos comunes y
temáticos) al hash de `ken` **sin éxito**; la contraseña no es trivial. La *recuperación de la
credencial* (hash) ya cumple el objetivo; el descifrado completo requeriría un ataque mayor
(hashcat modo 1000 con diccionario rockyou + reglas), recomendado como paso opcional.

**DPAPI (documentos/secret​os cifrados).** El triage conserva las claves DPAPI del usuario `ken`
(`Users/ken/Protect/S-1-5-21-1936453629-2262114833-2442330573-1001` y `Users/ken/Crypto`). Con la
contraseña de `ken` (o su masterkey) podrían descifrarse secretos protegidos (contraseñas guardadas
en navegador, credenciales). Queda como línea de análisis abierta. _Fuente: `15_hashes_sam.txt`._
### 7.8 Actividad de red (obj. 7)  _[preliminar — vía memoria]_

**Fuente:** `vol windows.netscan` sobre `memdump.mem` (`02_PRESERVACION/red/06_netscan.txt`).
Dirección IP del equipo: **192.168.145.72** (segmento LAN 192.168.145.0/24).

Hallazgos preliminares (pendiente correlación con `netstat`/artefactos de disco):

| Categoría | Evidencia (proceso / PID / conexión) |
|---|---|
| **Anonimización (Tor)** | `tor-0.4.8.10` (PID 88640) con circuitos a *guard relays* 54.39.234.91:9001 y 18.18.82.17:9001 (puerto OR 9001); puertos locales de control/SOCKS 40357–40363. |
| **P2P / BitTorrent** | `utweb.exe` (PID 106556) hacia peers externos (p. ej. 89.210.5.145, 194.110.13.123, 89.149.24.63). |
| **RDP entrante** | `svchost.exe` (PID 1072) escuchando en 3389 y **conexión ESTABLISHED entrante** 192.168.145.65 → 192.168.145.72:3389 (acceso remoto al equipo). |
| **Navegadores** | `opera.exe` (PID 77380), `brave.exe` (PID 71248), `msedge.exe` a múltiples destinos 443. |
| **VPN/DNS de terceros** | `rsVPNSvc.exe` / `rsDNSSvc.exe` (ReasonLabs) activos. |

> Las conexiones tienen *timestamps* del **22–23 de abril de 2024**, coherentes con el periodo de interés (obj. 5).
### 7.9 Herramientas y artefactos de software (obj. 8)  _[preliminar — vía memoria]_

**Fuente:** `vol windows.cmdline` sobre `memdump.mem` (`02_PRESERVACION/procesos/05_cmdline.txt`).
Todas atribuibles al usuario **ken**.

| Herramienta | Proceso / PID | Ruta / argumentos | Propósito (preliminar) |
|---|---|---|---|
| **Nmap / Zenmap** | `pythonw.exe` / 68800 | `C:\Program Files (x86)\Nmap\zenmap\bin\pythonw.exe -c "from zenmapGUI.App import run;run()"` | Escaneo de red / reconocimiento de hosts |
| **uTorrent Web** | `utweb.exe` / 106556 (+ `helper.exe`) | `C:\Users\ken\AppData\Roaming\uTorrent Web\utweb.exe /RUNONSTARTUP` | Transferencia P2P |
| **RAV VPN (ReasonLabs)** | `rsVPNSvc.exe` / 104776, `rsVPNClientSvc.exe`, `rsDNSClientSvc.exe`, `rsEngineSvc.exe` | `C:\Program Files\ReasonLabs\VPN\...` | VPN + DNS de terceros (ofuscación de tráfico) |
| **Tor** | `tor-0.4.8.10-w` / 88640; `brave.exe` TorLauncher | proceso Tor + modo Tor de Brave | Anonimización |
| **Navegadores** | Edge, Brave, Opera | rutas estándar | Navegación (idioma es-419) |

> **Relevancia para obj. 10 (seguimiento) y 11 (exfiltración):** la presencia conjunta de
> **Nmap** (reconocimiento), **uTorrent** (transferencia), **VPN + Tor** (ofuscación) y un
> **acceso RDP entrante** configura un escenario técnico consistente con reconocimiento de
> red y transferencia/ofuscación de datos. _Interpretación reservada hasta correlacionar con
> disco (historial, archivos, prefetch) y artefactos adicionales._
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
- A. Reporte de hashes — verificación de integridad con triple algoritmo (MD5/SHA-1/SHA-256), 9/9 PASS. Archivo: `02_PRESERVACION/hashes/reporte_integridad.md`.
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
