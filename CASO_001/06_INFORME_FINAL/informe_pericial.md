# INFORME PERICIAL EN INFORMÁTICA FORENSE
### Caso 24042024-001-Pavana-Hidalgo

> **Informe completo (contenido).** Redactado en Markdown; **pendiente de exportar a PDF**
> para la entrega final y de **firma/credenciales** del perito. Todas las secciones de análisis
> y conclusiones están redactadas con hallazgos verificables y referencias cruzadas a los Anexos.

---

## Portada
- **Título:** Informe Pericial en Informática Forense — Análisis de imagen forense de equipo de cómputo
- **Número de caso:** 24042024-001-Pavana-Hidalgo
- **Entidad solicitante:** Fiscalía General del Estado — Dirección de Peritos y Ciencias Forenses
- **Fiscal:** Lic. Alessandro Tapia Ochoa
- **Equipo pericial (peritos terceros designados):**
  - Diego Morales Gómez — 0250015@up.edu.mx
  - Ramón Andrés Galindo Gerardo — 0248040@up.edu.mx
  - Luis Atristain Alfaro — 0246760@up.edu.mx
  - Montserrat Castillo Vega — 0255627@up.edu.mx
  - Fernando Mauricio Chavarría Reyes — 0253214@up.edu.mx
  - Cecilia Gaona Vidales — 0267688@up.edu.mx
  - José Gabriel Hernández Castresana — 0253264@up.edu.mx
- **Fecha de emisión:** 2 de junio de 2026
- _(Imagen corporativa / logo)_

---

## 1. Resumen Ejecutivo

A solicitud de la Fiscalía General del Estado se realizó el análisis forense de los indicios
obtenidos de un equipo de cómputo (laptop) relacionado con el caso **24042024-001-Pavana-Hidalgo**:
una **imagen de disco** (EnCase E01), un **volcado de memoria RAM** y un **triage de registro** de
Windows. El análisis se condujo conforme a NIST SP 800-86 e ISO/IEC 27037/27041/27042, trabajando
sobre copias y certificando la integridad de toda la evidencia.

**Integridad:** verificada al 100% — la imagen de disco coincide (MD5/SHA-1 *Match*, sin sectores
defectuosos) y los nueve indicios crudos (memoria + hives) dieron **PASS** por triple algoritmo.

**Equipo:** laptop con **Windows 10 Pro 22H2**, hostname **DESKTOP-2TQHS9Q**, usuario **ken**;
el sistema fue **instalado/preparado el 21 de abril de 2024**, justo al inicio del periodo investigado.

**Conclusión principal:** entre el **21 y el 23 de abril de 2024**, el usuario `ken` utilizó el
equipo para **actividades de reconocimiento e inteligencia y para la recopilación masiva de datos
personales de terceros**. En concreto se evidenció: instalación y uso de herramientas de
**escaneo/pentesting** (Nmap, Parrot Security en VirtualBox, adaptador WiFi USB, material de
*wireless pentesting*); **reconocimiento OSINT** (uso de Censys para investigar un host con RDP
expuesto, 192.100.201.235); y la **descarga dirigida de decenas de archivos de nómina y personal**
desde portales gubernamentales (`.gob.mx` y otros), almacenados localmente. Se confirmó la presencia
y uso de **múltiples vectores de exfiltración** (varias memorias USB, cliente FTP FileZilla, P2P
uTorrent, OneDrive) y de **canales de anonimización** (Tor y VPN). Se recuperaron además las
credenciales (hashes NT) de las cuentas locales.

Finalmente, se identificaron **inconsistencias en la cadena de custodia** y un hallazgo relevante:
en la propia imagen quedó registrada **actividad de la unidad de destino del perito sobre el sistema
en vivo durante la recolección** (23-abr 10:12–10:13), lo que debe valorarse para la integridad
procesal. Los hallazgos se sustentan en evidencia verificable y reproducible (Anexos).

---

## 2. Introducción

- **Contexto del caso:** La Fiscalía General del Estado, en el marco de la investigación
  **24042024-001-Pavana-Hidalgo**, remitió para análisis pericial los indicios extraídos de una
  laptop asegurada. Se sospecha que el equipo pudo emplearse para **seguimiento de personas** y para
  la **extracción/transmisión de información**. El presente dictamen establece, con base técnica, los
  hechos relevantes para el esclarecimiento.
- **Objetivos del peritaje:** se reproducen íntegros en §5 (12 objetivos).
- **Consideraciones para evitar sesgos:** el análisis se basa exclusivamente en evidencia
  verificable; las hipótesis se formulan de manera falsable; se documenta toda acción en bitácora
  (`BITACORA_PERICIAL.md`); se trabaja sobre copias con los originales en solo lectura; y se
  distingue explícitamente entre **hecho técnico** e **interpretación**, reservando esta última
  cuando la evidencia no es concluyente.
- **Glosario breve:** *hash* (huella criptográfica de integridad); *OSINT* (inteligencia de fuentes
  abiertas); *DPAPI* (cifrado de datos por usuario en Windows); *BAM* (Background Activity Moderator,
  registro de ejecución de programas); *LNK* (archivo de acceso directo que registra accesos a
  archivos/carpetas); *artefacto* (rastro digital con valor probatorio).

---

## 3. Metodología
- **Marco:** NIST SP 800-86; ISO/IEC 27037 (adquisición/preservación), 27041 (metodología), 27042 (análisis e interpretación); Guía del Primer Respondiente (INTERPOL); SWGDE.
- **Fases:** Identificación → Preservación → Recolección → Análisis → Reporte.
- **Herramientas (con versión):**
  - **FTK Imager 4.7.3.81** (Exterro) — verificación de integridad de la imagen E01.
  - **Volatility 3 Framework 2.28.0** — análisis del volcado de memoria.
  - **Autopsy 4.23.1** (The Sleuth Kit) — análisis de la imagen de disco.
  - **Python 3.13.6** + `hashlib` (integridad), `regipy` (lectura de hives) y `pycryptodome`
    (AES/DES) — verificación de hashes y extractor propio de credenciales.
  - PowerShell `Get-FileHash` — respaldo visual de integridad.
- **Preservación:** verificación por *hashing* (MD5/SHA-1/SHA-256) contra los valores documentados;
  originales (`.E01`, `.mem`, hives) en **solo lectura**; todo el trabajo sobre copias.
- **Nota:** se evitó deliberadamente desactivar los controles de seguridad del equipo de análisis;
  cuando el antivirus bloqueó una utilidad estándar (impacket), se sustituyó por un script propio
  auditable en lugar de crear exclusiones (ver §7.7).

### 3.1 Marco normativo y su aplicación

Cada referencia obligatoria se aplica de forma concreta en este peritaje:

| Referencia | Cómo/dónde se aplica en este caso |
|---|---|
| **Guía del Primer Respondiente — INTERPOL** | Recepción, identificación e inventario inicial de indicios y manejo sin alteración (Fase 1, §4 y `01_IDENTIFICACION/informe_preliminar.md`). |
| **NIST SP 800-86** *(la solicitud cita "800-80"; la norma forense vigente es la **SP 800-86**, "Guide to Integrating Forensic Techniques into Incident Response")* | Marco de fases Identificación→Preservación→Recolección→Análisis→Reporte (§3); *hashing* de integridad (§7.1); análisis de memoria (§7.7–7.8). |
| **ISO/IEC 27037:2012** | Adquisición y **preservación**: trabajo sobre copias, originales en solo lectura, verificación por hash y continuidad de custodia (§5, §7.1, `05_CUSTODIA/`). |
| **ISO/IEC 27041** | **Idoneidad y reproducibilidad** del proceso: métodos validados, scripts documentados y bitácora trazable (§3, `BITACORA_PERICIAL.md`). |
| **ISO/IEC 27042** | **Análisis e interpretación**: hipótesis falsables, separación hecho/interpretación e interpretación reservada cuando no es concluyente (§6, §7, §9). |
| **Código Nacional de Procedimientos Penales** (arts. 227–228) | Cadena de custodia y **mismidad** de la evidencia; observaciones de custodia (§5, §7.12, `05_CUSTODIA/`). |
| **LFPDPPP** | Valoración legal del **acopio de datos personales de terceros** (nóminas/personal) hallado (§7.10) y recomendación asociada (§10). |

_Las referencias completas y los artículos científicos se listan al final del documento._

### 3.2 Fundamento jurídico y límites legales

México no cuenta con una ley única de informática forense, sino con un **marco normativo integrado**
(constitucional, procesal, penal y técnico) que regula la identificación, preservación, análisis y
presentación de la evidencia digital, garantizando su integridad, autenticidad y admisibilidad, y el
respeto a los derechos fundamentales (privacidad y debido proceso).

**a) Base legal de la actuación pericial.**
- **Art. 21 Constitucional:** la investigación de los delitos corresponde al Ministerio Público; la
  Fiscalía instruyó este peritaje mediante oficio.
- **CNPP, Art. 267, párr. 2:** *"Será materia de inspección todo aquello que pueda ser directamente
  apreciado por los sentidos… la policía se hará asistir por peritos"* — habilita la intervención del perito.
- **CNPP, prueba pericial (arts. 259–275):** el análisis es admisible si lo realiza un perito con
  **metodología científica reproducible** y dictamen fundamentado.
- **CNPP, prueba documental y material (arts. 380–387):** admite los **soportes electrónicos** como
  evidencia digital.

**b) Preservación, integridad y cadena de custodia.**
- **CNPP, Arts. 227–228 (cadena de custodia)** y **Art. 260** (fijación de indicios mediante
  **imágenes forenses verificadas con hash MD5/SHA-256**): documentación ininterrumpida y no
  modificabilidad de la evidencia original.
- **CNPP, Art. 212** (autenticidad e integridad de documentos electrónicos): exige demostrar la **no
  alteración** mediante funciones hash e imágenes bit a bit — cumplido en §7.1.
- **Normas técnicas mexicanas:** **NMX-I-27037-NYCE-2015** (≡ ISO/IEC 27037) y **NMX-I-289-NYCE-2016**
  (metodología de análisis forense), alineadas con **ISO/IEC 27041 y 27042**; su observancia es
  criterio de valoración judicial sobre la idoneidad técnica del proceso.

**c) Límite: comunicaciones privadas y datos almacenados en el dispositivo.**
- **Art. 16 Constitucional (párr. 12–13):** las **comunicaciones privadas son inviolables**; su
  intervención exige **mandamiento judicial** escrito, fundado y motivado (salvo aportación
  voluntaria de un participante). La evidencia obtenida ilícitamente se **excluye** (doctrina de
  exclusión, reforzada por la SCJN).
- **CNPP, Arts. 251–252 y 291–292:** la intervención de comunicaciones privadas requiere
  **autorización del Juez de control**, con solicitud fundada y motivada (persona, lugar, tipo y
  duración).
- **Jurisprudencia SCJN — Contradicción de tesis 194/2012:** la inviolabilidad de las comunicaciones
  privadas **se extiende a los datos almacenados** en un dispositivo asegurado a una persona sujeta a
  investigación; y **Tesis 1a./J. 9/2017** (requisitos constitucionales de la intervención).
- **Implicación para este caso:** el dictamen se practicó sobre un **dispositivo asegurado
  lícitamente** y por **instrucción ministerial**, limitándose a **artefactos del sistema, metadatos y
  archivos** (registro, ejecución de programas, historial web, USB, descargas). **No** se accedió al
  **contenido de comunicaciones privadas** (mensajería/correo), lo que habría requerido autorización
  judicial; de requerirse, debe canalizarse al MP / Juez de control.

**d) Tratamiento de los datos personales hallados.**
- Los archivos de **nómina/personal** (§7.10) contienen **datos personales de terceros** (nombres,
  percepciones, cuentas). Su tratamiento por la autoridad debe observar **licitud, finalidad,
  proporcionalidad y confidencialidad** (marco de protección de datos personales; **LFPDPPP** para
  particulares). El equipo pericial los trata **solo** para los fines del peritaje y bajo reserva.

**e) Posible relevancia penal de la conducta analizada** (marco de referencia, **sin prejuzgar**; la
calificación jurídica corresponde al MP y al órgano jurisdiccional):
- **Código Penal Federal, Art. 211 Bis** (acceso ilícito a sistemas y equipos de informática): uso de
  Nmap/Shodan/Censys para reconocer hosts ajenos (§7.10).
- **Conductas TIC tipificadas (CPF):** *obtener o copiar información de sistemas sin autorización del
  titular* y *robo/difusión de información personal sin consentimiento* — encuadrables por el acopio
  de PII de terceros (§7.10–7.11); también revelación de secretos y fraudes electrónicos.

---

## 4. Descripción de los Indicios
| Indicio | Tipo | Detalle | Estado recepción |
|---|---|---|---|
| 001 | Memoria volátil | `memdump.mem`, 9.0 GB, RAM 8 GB | ✅ Íntegro (PASS, §7.1) |
| 003 | Imagen de disco | `001-003-LAptop-Pavana T3.E01`, EnCase E01 (~465 GiB lógicos) | ✅ Íntegro (Match, §7.1) |
| — | Hives de registro | SAM, SECURITY, SYSTEM, SOFTWARE, DEFAULT, NTUSER/UsrClass (ken, Default) | ✅ Íntegros (9/9 PASS) |
| — | Disco origen | Seagate ST950042 0AS, S/N 5VJ8Z5ZN | Documental (custodia) |

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

Formuladas de manera **falsable** (pueden ser refutadas por la evidencia):

- **Hipótesis general (H0):** *El equipo `DESKTOP-2TQHS9Q` (usuario ken) fue utilizado, entre el 21
  y el 23 de abril de 2024, para actividades de reconocimiento/inteligencia y para la recopilación
  de datos personales de terceros, contando con medios para su exfiltración.*
  - *Sería refutada* si no existieran herramientas de reconocimiento, ni recopilación dirigida de
    datos de personas, ni vectores de salida de información.
- **Hipótesis de apoyo:**
  - **H1 (herramientas):** se instalaron y usaron utilidades de escaneo/pentesting (Nmap, Parrot
    Security, adaptador WiFi). *Refutable* si no hubiera rastros de instalación/ejecución.
  - **H2 (objetivo de reconocimiento):** se investigó al menos un host/objetivo concreto mediante
    OSINT. *Refutable* si no hubiera consultas dirigidas (Censys/buscadores) a un objetivo.
  - **H3 (acopio de datos personales):** se descargaron de forma dirigida documentos con datos de
    personas. *Refutable* si las descargas fueran aleatorias o sin relación con datos personales.
  - **H4 (capacidad de exfiltración):** existían y se usaron medios para extraer/transmitir
    información. *Refutable* si no hubiera medios USB, FTP, P2P, nube ni canales anonimizados.
  - **H5 (anonimización):** se emplearon mecanismos para ocultar el origen del tráfico. *Refutable*
    si no hubiera Tor/VPN activos.

> Cada hipótesis se contrasta con los hallazgos en §8 y se resuelve en §9.

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
NIST SP 800-86, ISO/IEC 27037 y **CNPP arts. 212 y 260** (autenticidad e integridad mediante hash e
imagen forense verificada). **Objetivo 9 cubierto.**
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

**Identificación del equipo (Autopsy → OS Information, sobre el registro del disco):**

| Dato | Valor |
|---|---|
| Nombre del equipo (hostname) | **DESKTOP-2TQHS9Q** |
| Edición | **Windows 10 Pro** (x64 / AMD64) |
| Titular registrado (Owner) | **ken** |
| Product ID | 00331-10000-00001-AA087 |
| Directorio del sistema | C:\Windows |

> El disco origen, según cadena de custodia, es **Seagate ST950042 0AS, S/N 5VJ8Z5ZN**
> (ver §7.3). La edición exacta y la **fecha de instalación del SO (2024-04-21)** se detallan
> en §7.4 a partir del hive SOFTWARE.

_Fuentes: `02_PRESERVACION/memoria/01_info.txt` y Autopsy OS Information
(`03_ANALISIS/autopsy_export/27_os_info.csv`)._
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
- ⚠️ **Hallazgo:** aparece un **segundo SID de usuario con identificador de equipo distinto** —
  `S-1-5-21-3933942852-973373972-2766786355-1032` (RID 1032). **Verificado contra el `ProfileList`
  del hive SOFTWARE: el único perfil humano del equipo es `ken` (…-1001); este segundo SID NO
  existe como perfil ni como cuenta local (SAM).** Por tanto su presencia se debe a **propiedad de
  archivos originados en otro sistema/usuario** (datos traídos desde otra máquina), lo que es
  relevante para los objetivos 4, 10 y 12.
- ✅ **Resuelto (Keyword Search, Autopsy):** la búsqueda del SID en la imagen lo localiza asociado
  a una cuenta **`installuser`** dentro del **hive SOFTWARE** y su log (`SOFTWARE.LOG1`), además de
  un punto de restauración (*System Volume Information*) y espacio **no asignado** — **no** en el
  `ProfileList`/SAM activos. Es decir, es un **remanente de provisión/despliegue**: esta instalación
  de Windows se generó a partir de una **imagen maestra preparada en otra máquina** por la cuenta de
  build `installuser`. Esto **refuerza** que el equipo fue **preparado/clonado el 21-abr-2024** para
  la actividad (no un equipo de uso prolongado). _Fuente: `03_ANALISIS/autopsy_export/29_keyword_SID_externo_installuser.csv`._

**Verificación de cuentas ocultas (obj. 4/12).** Se revisaron los dos vectores habituales de
ocultamiento de cuentas: (1) la enumeración completa del **SAM** (`…\Account\Users\Names` y los
RID en `…\Account\Users`) y (2) la clave **`SOFTWARE\…\Winlogon\SpecialAccounts\UserList`** (que
oculta cuentas de la pantalla de inicio). **Resultado:** el SAM contiene **exactamente 5 cuentas**
(Administrador 500, Invitado 501, DefaultAccount 503, WDAGUtilityAccount 504, **ken 1001**), sin
cuentas terminadas en `$` ni RID adicionales; y **la clave `SpecialAccounts\UserList` no existe**.
Por tanto **no hay usuarios ocultos** en el equipo, y el segundo SID (`…-1032`) **no es una cuenta
local** (no figura en el SAM). _Script: `03_ANALISIS/correlacion/revisar_usuarios_ocultos.py`._

**Titular e instalación del SO (hive SOFTWARE → `Microsoft\Windows NT\CurrentVersion`):**

| Dato | Valor |
|---|---|
| Producto / edición | **Windows 10 Pro** (Professional), **22H2** (build **19045**) |
| **Titular registrado (RegisteredOwner)** | **ken** |
| Organización registrada | (vacía / "0") |
| Product ID | 00331-10000-00001-AA087 |
| **Fecha de instalación (InstallDate)** | epoch 1713758775 = **2024-04-22 04:06:15 UTC** = **2024-04-21 22:06 (UTC−6)** |

**Interpretación (obj. 4):** el sistema operativo actual fue **instalado/configurado el
2024-04-21**, al inicio mismo de la ventana de actividad (21–24 abr), bajo el titular **ken**.
Esto indica que el equipo fue **preparado expresamente** en ese momento (no un equipo de uso
prolongado previo), coherente con que las herramientas (Nmap, VirtualBox, VPN, navegadores) se
instalaran ese mismo 21–23 de abril (§7.9).

> *Nota de versión:* el registro reporta **build 19045 (22H2)**; Volatility (`windows.info`)
> reporta el identificador base **15.19041** del kernel 2004. Ambos corresponden a Windows 10;
> se toma como autoritativa la del registro (22H2/19045). _Fuente: hive SOFTWARE._
### 7.5 Actividad durante/posterior a la adquisición (obj. 3)

**Hallazgo crítico (artefactos LNK / Recent Documents, Autopsy).** Dentro de la imagen del
disco quedaron registrados accesos de Explorador, fechados **2024-04-23 10:12–10:13**, a la
**carpeta del propio caso forense** desde una unidad externa **D:**:

| LNK (acceso reciente) | Ruta destino | Fecha/hora |
|---|---|---|
| `TOSHIBA EXT (D).lnk` | `D:\` | 2024-04-23 10:12:12 |
| `Caso-Pavana-Hidalgo.lnk` | `D:\Caso-Pavana-Hidalgo` | 2024-04-23 10:12:12 |
| `Laptop Dell.lnk` | `D:\Caso-Pavana-Hidalgo\Laptop Dell` | 2024-04-23 10:13:04 |
| `Triage.lnk` | `D:\Caso-Pavana-Hidalgo\Laptop Dell\Triage` | 2024-04-23 10:13:04 |
| `Dump memoria.lnk` | `D:\Caso-Pavana-Hidalgo\Laptop Dell\Dump memoria` | 2024-04-23 10:13:23 |
| `Imagen de disco.lnk` | `D:\Caso-Pavana-Hidalgo\Laptop Dell\Imagen de disco` | 2024-04-23 10:13:33 |

Correlación: el dispositivo USB **Toshiba B301, S/N `20220817001348F`** (la **misma unidad de
destino forense** declarada en la cadena de custodia) se conectó al equipo a las
**2024-04-23 10:37:33** (§7.9/USB). El **volcado de memoria** se tomó a las **10:17** y la
**imagen de disco** inició a las **11:10**.

**Interpretación (obj. 3 y 12):** la estructura de carpetas del caso (`Caso-Pavana-Hidalgo\…\
Triage`, `Dump memoria`, `Imagen de disco`) fue **navegada/creada en el sistema en vivo** antes
de finalizar la adquisición, y esos artefactos quedaron **embebidos en la propia imagen**. Es
decir, **sí existió actividad de manipulación sobre el sistema encendido durante el proceso de
recolección** (montaje de la unidad de destino del perito y navegación del árbol de evidencia).
Esto es esperable en una adquisición *en vivo*, pero **debe constar**: contradice una imagen
"limpia" previa a toda interacción y es relevante para valorar la cadena de custodia (§7.12).

### 7.6 Línea de tiempo 20–24 abr 2024 (obj. 5)

Cronología reconstruida (registro, BAM, historial web, descargas, LNK; hora local UTC−6):

| Fecha/hora | Evento |
|---|---|
| 2019-12-07 | Instalación base del SO (componentes Windows). |
| **2024-04-21 16:21–16:31** | **Primer arranque/OOBE del perfil** (FirstLogonAnim, CloudExperienceHost) — alta del usuario `ken`. |
| 2024-04-21 19:52–20:17 | Descarga e instalación de **Nmap 7.94** + **Npcap**; descarga de **Parrot Security 5.3 OVA**, **FileZilla**, **7-Zip**, **VirtualBox**. |
| 2024-04-22 00:00–02:44 | Ejecución de **VirtualBox/VirtualBoxVM**; instalación de VirtualBox 7.0.14. |
| 2024-04-22 11:39–12:02 | Búsquedas **"osint framework"**, **"censys"**; consulta en **Censys** del host **192.100.201.235** (servicio **RDP/3389**). |
| 2024-04-22 11:28–17:31 | Instalación de **Opera**, **Brave** (modo Tor), **DuckDuckGo**; **RAV VPN/Endpoint**. |
| 2024-04-22 20:58–21:06 | Búsquedas **"armerias en estados unidos"**, **"funda escuadra"**, **"canana"**, **"gabardina"**. |
| 2024-04-22 23:11–23:24 | Conexión USB **SanDisk**; instalación **uTorrent Web**; uso de **cmd**, **mstsc** (RDP), **notepad**. |
| **2024-04-23 08:35–09:05** | **Descarga masiva de archivos de nómina/personal** desde decenas de sitios .gob.mx (y .gov.co/.cl) hacia `C:\Users\ken\Documents`. |
| 2024-04-23 09:50–10:16 | Conexión de **adaptador WiFi USB Ralink** y **memorias Verbatim/Lexar**. |
| 2024-04-23 10:12–10:13 | Navegación de la **carpeta del caso forense en D:** (ver §7.5). |
| 2024-04-23 10:17 / 11:10 | **Adquisición**: volcado de memoria / inicio de imagen de disco. |

_Fuentes: `25_run_programs.csv`, `22_web_downloads.csv`, `21_web_history.csv`, `26_recent_documents.csv`, `23_usb_devices.csv`._

> **Corroboración visual:** el *Timeline Snapshot* de Autopsy (`03_ANALISIS/timeline/timeline_autopsy_snapshot.png`)
> grafica la concentración de eventos el 21–23 abr 2024 (instalación de Nmap, visitas a `shodan.io`,
> consultas a las IPs objetivo, descargas de nómina, etc.). Ver Anexo.
### 7.7 Credenciales y cifrado / DPAPI (obj. 6)

> **Encuadre jurídico (§3.2).** La recuperación de credenciales se realiza como **prueba pericial**
> (CNPP arts. 259–275) por **instrucción ministerial**, sobre un dispositivo asegurado lícitamente y
> al amparo del objetivo 6 del oficio. **No** se accedió al contenido de comunicaciones privadas
> —protegido aun en dispositivos asegurados (Art. 16 Constitucional; SCJN, Contradicción de tesis
> 194/2012)— lo que exigiría autorización judicial (CNPP arts. 291–292).

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

**Descifrado de contraseña — LOGRADO.** Tras un primer diccionario temático sin éxito, se ejecutó
un ataque contra el diccionario **rockyou** (14,344,391 entradas) calculando el hash NT
(`MD4(UTF-16LE)`) de cada candidato. La contraseña de **`ken` se recuperó en claro**:

> **Contraseña de `ken`: `MyPassword`** (NT `f12c418083c05e3a7de78582e61f652d`, hallada en ~24 s).

Script reproducible: `03_ANALISIS/correlacion/descifrar_password_ken.py`. **Objetivo 6 cumplido en
su totalidad** (hash recuperado + contraseña descifrada).

**DPAPI (secretos cifrados) — EJECUTADO.** Con la contraseña recuperada (`MyPassword`) y el SID de
`ken`, se **descifró la masterkey DPAPI** del usuario (`2402689c-5e8c-4083-8474-015e1fa1cb5a`, del
triage) mediante `dpapick3`. Con ella se obtuvo la **clave AES de cifrado de credenciales** (32 bytes)
de **Brave y de Edge** (desde sus archivos `Local State`, esquema *App-Bound v10*), y se intentó
descifrar el almacén `Login Data` de cada navegador.

**Resultado:** la cadena de descifrado funcionó (masterkey y claves AES obtenidas), pero las tablas
`logins` de **Brave y Edge están vacías (0 credenciales guardadas)**. Es decir, **`ken` no almacenó
contraseñas en los navegadores** —conducta coherente con el uso de Tor/VPN y prácticas de
ocultamiento—. Se documenta el procedimiento y el resultado negativo por completitud.

Script reproducible: `03_ANALISIS/correlacion/descifrar_dpapi_navegador.py`
(salida: `16_credenciales_navegador.txt`).
_Fuentes: `15_hashes_sam.txt`, `descifrar_password_ken.py`, claves DPAPI del triage, archivos
`Local State`/`Login Data` en `autopsy_export/dpapi/`._

**Documentos cifrados (revisión).** Autopsy marcó **6 archivos** por alta entropía
(*Encryption Suspected*). Tras su revisión, **ninguno es un documento del usuario cifrado para
ocultar información**; todos tienen explicación legítima: un **instalador MSI** de LibreOffice
(comprimido), el **caché de iconos** de Windows (`iconcache_256.db`, `IconCache.db-slack`) y tres
**bases internas del navegador DuckDuckGo** (`browser-v1.db`, `dbp-v1.db`, `favicons-v1.db`). Se
concluye que **no existen documentos cifrados de interés** ocultos por el usuario.
_Fuente: `03_ANALISIS/autopsy_export/28_encryption_suspected.csv`._
### 7.8 Actividad de red (obj. 7)

**Fuente:** `vol windows.netscan` sobre `memdump.mem` (`02_PRESERVACION/red/06_netscan.txt`),
**corroborado** con el historial web y las herramientas hallados en disco (§7.9–7.11).
Dirección IP del equipo: **192.168.145.72** (segmento LAN 192.168.145.0/24).

Hallazgos (red entrante y saliente):

| Categoría | Evidencia (proceso / PID / conexión) |
|---|---|
| **Anonimización (Tor)** | `tor-0.4.8.10` (PID 88640) con circuitos a *guard relays* 54.39.234.91:9001 y 18.18.82.17:9001 (puerto OR 9001); puertos locales de control/SOCKS 40357–40363. |
| **P2P / BitTorrent** | `utweb.exe` (PID 106556) hacia peers externos (p. ej. 89.210.5.145, 194.110.13.123, 89.149.24.63). |
| **RDP entrante** | `svchost.exe` (PID 1072) escuchando en 3389 y **conexión ESTABLISHED entrante** 192.168.145.65 → 192.168.145.72:3389 (acceso remoto al equipo). |
| **Navegadores** | `opera.exe` (PID 77380), `brave.exe` (PID 71248), `msedge.exe` a múltiples destinos 443. |
| **VPN/DNS de terceros** | `rsVPNSvc.exe` / `rsDNSSvc.exe` (ReasonLabs) activos. |

> Las conexiones tienen *timestamps* del **22–23 de abril de 2024**, coherentes con el periodo de interés (obj. 5).
### 7.9 Herramientas y artefactos de software (obj. 8)

**Confirmación por disco (Autopsy — Installed/Run Programs, Web Downloads).** Además de lo visto
en memoria, el disco confirma y amplía el conjunto de herramientas, con fechas de descarga/instalación
en el periodo de interés (todas en el perfil de **ken**):

| Herramienta | Categoría | Evidencia (fecha) |
|---|---|---|
| **Nmap 7.94 + Npcap 1.75** | Escaneo de red / captura de paquetes | Descarga `nmap-7.94-setup.exe` de nmap.org (04-21 19:52); instalado 04-22 01:54 |
| **Parrot Security 5.3 (OVA)** | Distro de pentesting (en VM) | Descarga `Parrot-security-5.3_amd64.ova` de parrot.sh (04-21 19:57) |
| **Oracle VirtualBox 7.0.14** | Virtualización (ejecutar la VM) | Instalado 04-22 02:44; `VirtualBoxVM.exe` ejecutado 04-22 00:00 |
| **FileZilla 3.67** | Cliente FTP (transferencia) | Descargado 04-21; ejecutado 04-22 13:36 |
| **RAV VPN / RAV Endpoint / Safer Web** | VPN + DNS de terceros | Instalados 04-23 05:23–05:29 |
| **Tor** (proceso + Brave TorLauncher) | Anonimización | (memoria) |
| **uTorrent Web** | P2P | `utweb_installer` 04-22 23:22 |
| **Adaptador WiFi USB Ralink RT2870/RT3070** | Inalámbrico (monitor/inyección) | Conectado 04-23 09:50 |
| Brave / Opera / DuckDuckGo / Edge | Navegadores | 04-22 |
| **mstsc.exe** | Cliente RDP | Ejecutado 04-22 23:19 |

_Fuentes: `24_installed_programs.csv`, `25_run_programs.csv`, `22_web_downloads.csv`, `23_usb_devices.csv`._

---

**Fuente (memoria):** `vol windows.cmdline` sobre `memdump.mem` (`02_PRESERVACION/procesos/05_cmdline.txt`).
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
### 7.10 Seguimiento / recopilación sobre personas (obj. 10)

La evidencia de disco muestra dos vertientes de actividad de inteligencia/recopilación:

**a) Reconocimiento técnico (OSINT / escaneo).**
- Búsquedas en Brave: **"osint framework"** (2024-04-22 11:39) y **"censys"** (11:51).
- Uso de **Censys Search** (censys.io) para consultar el host **192.100.201.235**, revisando
  específicamente su servicio **RDP (3389/TCP)** (2024-04-22 12:02) — reconocimiento de un
  objetivo concreto con escritorio remoto expuesto.
- Uso de **Shodan** (`shodan.io`, **13 visitas**) — buscador de dispositivos expuestos en
  Internet, herramienta típica de reconocimiento; y consulta de un **segundo objetivo**, la IP
  **187.189.8.57** (rango mexicano). _(Evidenciado en el timeline de Autopsy, Anexo.)_
- Instalación/uso de **Nmap** y de un **adaptador WiFi USB Ralink RT2870/RT3070** (apto para
  monitoreo/inyección inalámbrica) y descarga de **"Mastering Kali Linux Wireless Pentesting.pdf"**.

**b) Recopilación masiva de datos personales (PII) de terceros.**
- El **2024-04-23 08:35–09:05** se descargaron **decenas de archivos de nómina y de personal**
  (`.xlsx`, `.xls`, `.docx`) desde numerosos portales gubernamentales e institucionales
  (tlajomulco, edomex, condusef, monterrey, guadalajara, puebla, **hidalgo.gob.mx**, cdmx, seph,
  banxico, scjn; y .gov.co/.cl), guardados en `C:\Users\ken\Documents` (p. ej.
  *"Copia-de-nomina-de-trabajadores.xlsx"*, *"Layout Dispersión de Nómina df.xlsm"*,
  *"3er_trimestre_cuentas_de_nomina_2022.xlsx"*). La búsqueda se hizo con operadores
  **`filetype:xlsx` / `filetype:docx`** en Bing — recolección dirigida de documentos con datos
  de empleados (nombres, percepciones, cuentas de dispersión).

> Estas dos vertientes (reconocimiento de hosts/red + acopio dirigido de datos de personas)
> son **consistentes con actividad de seguimiento/perfilamiento**. _Observación adicional:_ se
> registraron búsquedas de **"armerias en estados unidos"**, **"funda escuadra"**, **"canana"**
> y **"gabardina"** (2024-04-22 21:00) que, por su naturaleza, se documentan para conocimiento
> de la autoridad, reservando su interpretación.

> **Encuadre jurídico (§3.2).** El acopio dirigido de **datos personales de terceros** sin
> consentimiento contraviene los principios de **licitud y consentimiento** (LFPDPPP, Art. 6) y puede
> encuadrar en conductas del **Código Penal Federal** (*obtener o copiar información de sistemas sin
> autorización del titular*; *robo/difusión de información personal sin consentimiento*). El
> reconocimiento de hosts ajenos con Nmap/Shodan/Censys puede actualizar **acceso ilícito a sistemas
> y equipos de informática** (CPF, **Art. 211 Bis**). _Marco de referencia, sin prejuzgar; la
> calificación corresponde al MP/juez._

### 7.11 Exfiltración / transmisión de información (obj. 11)

Se identifican **múltiples vectores de salida de datos** disponibles y en uso en el periodo:

| Vector | Evidencia |
|---|---|
| **Almacenamiento USB** | Memorias **Lexar JumpDrive 16 GB** (S/N AA218R9MXJHI5V5E, 04-22), **SanDisk** (04-22 23:11), **Verbatim Flash Drive** (S/N 700031C37113A349, 04-23 10:15); además USB **Ventoy (E:)** con archivo `vpn.txt`. |
| **FTP** | **FileZilla 3.67** descargado y ejecutado (cliente FTP, 04-22 13:36) — transferencia de archivos. |
| **P2P** | **uTorrent Web** instalado y activo (memoria + disco). |
| **Nube** | **OneDrive** en ejecución (`OneDrive.exe`, 04-22 16:32). |
| **Canales anonimizados** | **Tor** (proceso + Brave) y **RAV VPN** activos (§7.8) — ofuscan el origen/destino del tráfico. |

Los **archivos de nómina/personal** descargados (§7.10) quedaron **almacenados localmente en
`C:\Users\ken\Documents`**, disponibles para su transferencia por cualquiera de los vectores
anteriores. La presencia de `E:\vpn.txt` (en USB Ventoy) sugiere credenciales/listas de VPN
guardadas en medio extraíble.

> **Demostración técnica:** existe evidencia clara de **capacidad y preparación de exfiltración**
> (medios USB conectados, cliente FTP, P2P, nube, canales anonimizados) y de **acopio de datos de
> terceros**. La confirmación de una transferencia *consumada* de un archivo específico hacia un
> destino externo requeriría correlación adicional (logs de FileZilla, contenido de los USB, o
> capturas de red), que se señala como línea de profundización.

### 7.12 Inconsistencias en los indicios (obj. 12)

1. **Disco:** la cadena de custodia declara **500 GB / 38,913 cilindros**, pero la imagen reporta
   **~465 GiB (976,773,152 sectores) / 60,801 cilindros** y tipo "USB Device". (El conteo de
   sectores sí es coherente entre FTK y Autopsy.)
2. **Fecha de adquisición de memoria:** la custodia indica **"24-Abril-2014 10:26"** (año 2014
   erróneo); la evidencia técnica (Volatility SystemTime + *Created Time* del `.mem`) sitúa la
   captura el **23-abril-2024 ~10:17**.
3. **Fecha de adquisición de disco:** custodia **15-Abril-2024 11:10** vs. cabecera/notas FTK del
   `.E01` **23-Abril-2024 11:10** (coincide la hora, discrepa el día).
4. **Hashes de la copia forense en blanco** en el formato de cadena de custodia (aunque la
   integridad sí se verificó: E01 *Match* y 9/9 hives PASS).
5. **Herramienta:** verificación con **Exterro FTK Imager 4.7.3.81** vs. adquisición con
   **AccessData FTK Imager 4.7.2.11**.
6. **Actividad peri-adquisición embebida en la imagen** (§7.5): la carpeta del caso (`D:\Caso-
   Pavana-Hidalgo\…`) fue navegada en el sistema en vivo 2024-04-23 10:12–10:13, antes de concluir
   la recolección.
7. **Segundo SID de usuario** ajeno al equipo (`S-1-5-21-3933942852-973373972-2766786355-1032`),
   sin cuenta local en SAM/ProfileList: corresponde a la cuenta de build **`installuser`** de otra
   máquina, hallada como **remanente en el hive SOFTWARE** → indica **despliegue desde imagen
   maestra** (equipo preparado/clonado). Ver §7.4.

_Fundamento: buenas prácticas NIST SP 800-86, ISO/IEC 27037/27042, ENFSI/SWGDE; se documentan
sin alterar la evidencia._

---

## 8. Hallazgos Clave

Relación de la evidencia con cada hipótesis (§6):

| # | Hallazgo clave | Evidencia (fuente) | Hipótesis |
|---|---|---|---|
| HC-1 | Integridad de toda la evidencia certificada (E01 *Match*; 9/9 hives PASS) | §7.1, Anexo A | — (base) |
| HC-2 | Equipo Windows 10 Pro 22H2, hostname DESKTOP-2TQHS9Q, usuario **ken**, **instalado 21-abr-2024** | §7.2, §7.4 | contexto |
| HC-3 | Instalación/uso de **Nmap+Npcap, Parrot Security (VM), adaptador WiFi USB**, material de wireless pentesting | §7.9, `24/25_*.csv` | **H1** ✔ |
| HC-4 | **Reconocimiento OSINT**: Censys del host **192.100.201.235** (RDP/3389), **Shodan** (13 visitas) y consulta de la IP **187.189.8.57** | §7.10, `21_web_history.csv`, timeline | **H2** ✔ |
| HC-5 | **Descarga dirigida de decenas de archivos de nómina/personal** de portales `.gob.mx` (operadores `filetype:`) | §7.10, `22_web_downloads.csv` | **H3** ✔ |
| HC-6 | **Vectores de exfiltración** presentes y usados: 3 memorias USB, FileZilla FTP, uTorrent, OneDrive | §7.11, `23_usb_devices.csv` | **H4** ✔ |
| HC-7 | **Anonimización** activa: Tor (proceso + Brave) y RAV VPN | §7.8, §7.9 | **H5** ✔ |
| HC-8 | **RDP entrante** establecido desde 192.168.145.65 | §7.8, `06_netscan.txt` | H2/H4 |
| HC-9 | Credenciales recuperadas: hashes NT + **contraseña de `ken` descifrada (`MyPassword`)** + masterkey DPAPI descifrada (sin contraseñas guardadas) | §7.7, `15_hashes_sam.txt`, `16_credenciales_navegador.txt` | obj. 6 |
| HC-10 | **Actividad peri-adquisición** (carpeta del caso en D: navegada en vivo 23-abr 10:12–10:13) + 7 inconsistencias de custodia | §7.5, §7.12 | obj. 3/12 |

> Las cinco hipótesis de apoyo (H1–H5) quedan **corroboradas** por evidencia concurrente de
> memoria, registro y disco, lo que sustenta la hipótesis general H0.

---

## 9. Conclusiones

Con base en la evidencia verificable y reproducible analizada, y de forma **simétrica** con las
hipótesis planteadas:

1. **(H0 — confirmada)** El equipo `DESKTOP-2TQHS9Q`, bajo el usuario **ken**, fue empleado entre el
   **21 y el 23 de abril de 2024** para **reconocimiento técnico/OSINT** y para la **recopilación
   dirigida de datos personales de terceros** (archivos de nómina y personal de múltiples entidades
   gubernamentales), disponiendo de **medios para su exfiltración**.
2. **(Obj. 1, 2, 4)** Se identificó el equipo (Windows 10 Pro 22H2, hostname DESKTOP-2TQHS9Q,
   titular ken) y el disco (Seagate ST950042, S/N 5VJ8Z5ZN); el SO fue **instalado el 21-abr-2024**,
   indicando un equipo **preparado para la actividad**, no de uso prolongado previo.
3. **(Obj. 6, 7, 8)** Se recuperaron las credenciales locales (hashes NT); se reconstruyó la
   actividad de red (Tor, P2P, **RDP entrante**) y se identificaron las herramientas (Nmap, Parrot
   Security, VirtualBox, FileZilla, RAV VPN, uTorrent, adaptador WiFi USB).
4. **(Obj. 9)** La integridad de **todos** los indicios quedó **certificada** (NIST SP 800-86 /
   ISO 27037).
5. **(Obj. 3, 12)** Se documentó **actividad de la unidad de destino del perito sobre el sistema en
   vivo durante la recolección** y **siete inconsistencias** en la cadena de custodia; estos puntos
   **no invalidan** la integridad técnica verificada de las copias, pero **deben valorarse** en sede
   procesal.

**Limitaciones del análisis:**
- La **transferencia consumada** de un archivo concreto hacia un destino externo no se demostró de
  forma directa; sí la **capacidad, preparación y acopio** (se requeriría correlación con logs de
  FileZilla, contenido de los USB físicos —no aportados como indicio— o captura de red).
- La ingesta de Autopsy se interrumpió una vez por una excepción no fatal de la herramienta; se
  relanzó y los artefactos analizados son válidos y completos para los fines del dictamen.

---

## 10. Recomendaciones

1. **Asegurar y analizar los medios USB físicos** referidos (Lexar, SanDisk, Verbatim, Ventoy) para
   confirmar exfiltración consumada y el contenido de `vpn.txt`.
2. **Solicitar/correlacionar** registros de red perimetral y del host `192.100.201.235` para
   esclarecer el objetivo del reconocimiento (RDP).
3. **Subsanar la cadena de custodia** (fechas, hashes de la copia en blanco) y dejar constancia
   formal de la actividad peri-adquisición; en futuras diligencias, adquirir **sin interacción con
   el sistema en vivo** o documentarla con detalle.
4. Valorar implicaciones de **protección de datos personales** por el acopio de PII de terceros y la
   posible relevancia penal (CPF **Art. 211 Bis**; obtención/copia de información sin autorización del
   titular). Ver §3.2.
5. **Resguardo y confidencialidad** de los datos personales de terceros contenidos en la evidencia:
   tratarlos solo para los fines de la investigación, con acceso restringido y bajo reserva.
6. **Cotejar la numeración de los artículos** citados (§3.2) con el texto vigente de cada
   ordenamiento a la fecha de emisión, dado que las leyes se reforman periódicamente.

---

## 11. Anexos
- A. Reporte de hashes — integridad triple algoritmo (MD5/SHA-1/SHA-256), 9/9 PASS: `02_PRESERVACION/hashes/reporte_integridad.md`; capturas en `04_EVIDENCIA/capturas/`.
- B. Salidas de Volatility 3 (`02_PRESERVACION/{memoria,procesos,red}/`): `01_info`, `02_pslist`, `03_pstree`, `05_cmdline`, `06_netscan`, `07_cmdscan`, `08_consoles`.
- C. Exportaciones de Autopsy (`03_ANALISIS/autopsy_export/`): `21_web_history`, `22_web_downloads`, `23_usb_devices`, `24_installed_programs`, `25_run_programs`, `26_recent_documents`, `27_os_info`, `28_encryption_suspected` (CSV); **Timeline Snapshot** (`03_ANALISIS/timeline/timeline_autopsy_snapshot.png`).
- C-bis. Descifrado DPAPI de navegador (`03_ANALISIS/correlacion/`): `descifrar_dpapi_navegador.py` + `16_credenciales_navegador.txt`.
- D. Extracción de credenciales (`03_ANALISIS/correlacion/`): `extraer_hashes_sam.py` + `15_hashes_sam.txt`.
- E. Bitácora pericial completa: `BITACORA_PERICIAL.md` (33 actividades fechadas).
- F. Cadena de custodia: `24042024_001-003-Pavana-Hidalgo-RCDC.pdf`.

---

## 12. Firma y Credenciales

**Equipo pericial (peritos terceros designados).** Cada integrante suscribe el presente dictamen;
la firma electrónica avanzada y la constancia de idoneidad profesional se adjuntan por separado.

| # | Perito | Correo | Firma |
|---|---|---|---|
| 1 | Diego Morales Gómez | 0250015@up.edu.mx | __________________ |
| 2 | Ramón Andrés Galindo Gerardo | 0248040@up.edu.mx | __________________ |
| 3 | Luis Atristain Alfaro | 0246760@up.edu.mx | __________________ |
| 4 | Montserrat Castillo Vega | 0255627@up.edu.mx | __________________ |
| 5 | Fernando Mauricio Chavarría Reyes | 0253214@up.edu.mx | __________________ |
| 6 | Cecilia Gaona Vidales | 0267688@up.edu.mx | __________________ |
| 7 | José Gabriel Hernández Castresana | 0253264@up.edu.mx | __________________ |

- **Firma electrónica avanzada:** _[adjuntar por cada perito]_
- **Constancia de idoneidad profesional:** _[adjuntar por cada perito]_

---

## Referencias normativas y científicas

**Normativas y guías:**
- INTERPOL (2021). *Guidelines for Digital Forensics First Responders*.
- Kent, K., Chevalier, S., Grance, T. & Dang, H. (2006). **NIST SP 800-86** — *Guide to Integrating
  Forensic Techniques into Incident Response*. National Institute of Standards and Technology.
- **ISO/IEC 27037:2012** — *Guidelines for identification, collection, acquisition and preservation
  of digital evidence*; **ISO/IEC 27041:2015**; **ISO/IEC 27042:2015**.
- SWGDE (2018). *Best Practices for Computer Forensic Acquisitions*; ENFSI (2015). *Best Practice
  Manual for the Forensic Examination of Digital Technology*.
- **Constitución Política de los Estados Unidos Mexicanos** — Art. 16 (inviolabilidad de las
  comunicaciones privadas, párr. 12–13; protección de datos), Art. 20 (debido proceso / exclusión de
  prueba ilícita) y Art. 21 (investigación a cargo del MP).
- **Código Nacional de Procedimientos Penales** — inspección con auxilio de peritos (art. 267),
  prueba pericial (arts. 259–275), cadena de custodia (arts. 227–228) y fijación con hash (art. 260),
  autenticidad/integridad de documentos electrónicos (art. 212), intervención de comunicaciones
  privadas (arts. 251–252, 291–292) y prueba documental/material electrónica (arts. 380–387).
- **Código Penal Federal** — acceso ilícito a sistemas y equipos de informática (**Art. 211 Bis**);
  obtención/copia de información sin autorización del titular; revelación de secretos y fraudes electrónicos.
- **Ley Federal de Protección de Datos Personales en Posesión de los Particulares** (LFPDPPP) —
  principios de licitud y consentimiento (art. 6).
- **Normas técnicas mexicanas:** NMX-I-27037-NYCE-2015 (≡ ISO/IEC 27037) y NMX-I-289-NYCE-2016.
- **Jurisprudencia / criterios SCJN:** Contradicción de tesis 194/2012 (datos almacenados en
  dispositivo asegurado); Tesis 1a./J. 9/2017 (requisitos de intervención); Manual de Prueba Pericial
  Digital (SCJN); Guía Nacional de Cadena de Custodia de Evidencia Digital (FGR).

**Artículos científicos (≥2; se incluyen 3, cada uno aplicado a una parte del análisis):**
- Quick, D. & Choo, K-K. R. (2014). *Impacts of increasing volume of digital forensic data: A survey
  and future research challenges*. **Digital Investigation**, 11(4), 273–294.
  → *Sustenta el enfoque ante el gran volumen (imagen de ~465 GiB, memoria de 9 GB) y el uso de
  triage/exportaciones dirigidas (§3, §7).*
- Case, A. & Richard III, G. G. (2017). *Memory forensics: The path forward*. **Digital
  Investigation**, 20, 23–33.
  → *Fundamenta el análisis del volcado de memoria con Volatility 3 (§7.7, §7.8, §7.9).*
- Bursztein, E., Picod, J-M. & Audebert, R. (2010). *Recovering Windows Secrets and EFS Certificates
  Offline*. **USENIX WOOT '10** (Workshop on Offensive Technologies).
  → *Fundamenta la recuperación **offline** de credenciales: extracción de hashes del SAM con la
  SysKey/bootkey y descifrado de secretos protegidos por **DPAPI** (§7.7).*
- _(Opcional adicional)_ Carrier, B. (2003). *Defining digital forensic examination and analysis
  tools using abstraction layers*. **International Journal of Digital Evidence**, 1(4).
