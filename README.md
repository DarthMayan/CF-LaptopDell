# CF-LaptopDell — Peritaje Informático Forense
### Caso 24042024-001-Pavana-Hidalgo

Análisis forense de los indicios de una laptop, solicitado por la **Fiscalía General del Estado**
(Dirección de Peritos y Ciencias Forenses). Examen final de la asignatura de Cómputo Forense.

- **Perito:** Diego Morales Gómez — 0250015@up.edu.mx
- **Equipo analizado:** `DESKTOP-2TQHS9Q` — Windows 10 Pro 22H2 — usuario **ken**
- **Estándares:** NIST SP 800-86 · ISO/IEC 27037 / 27041 / 27042 · INTERPOL · SWGDE/ENFSI

---

## ⚠️ Evidencia pesada (no está en el repo)

Los archivos `memdump.mem` (9 GB) y `001-003-LAptop-Pavana T3.E01` (~40 GB) **no se versionan**
(exceden el límite de GitHub; ver `.gitignore`). Se conservan en local; **su integridad se acredita
con los hashes** documentados en los `.txt` y en `02_PRESERVACION/hashes/`. La base de datos de
Autopsy tampoco se versiona (solo sus exportaciones CSV).

---

## Estructura del repositorio

```
Laptop Dell/                  Indicios originales (PDFs, hashes, hives de triage)
│
CASO_001/                     Entregable estructurado del peritaje
├── PLAN_MAESTRO.md           Fases, mapa objetivo→evidencia→herramienta, estado
├── BITACORA_PERICIAL.md      Registro cronológico de las 25 actividades
├── 01_IDENTIFICACION/        informe_preliminar.md
├── 02_PRESERVACION/          Integridad + salidas de memoria
│   ├── hashes/               verificar_integridad.py, capturar_hashes.ps1, reporte_integridad.md
│   ├── memoria/ procesos/ red/   Salidas de Volatility 3
├── 03_ANALISIS/
│   ├── correlacion/          extraer_hashes_sam.py, 15_hashes_sam.txt
│   └── autopsy_export/        CSV exportados de Autopsy (web, USB, programas…)
├── 04_EVIDENCIA/capturas/    Capturas (integridad, FTK Verify)
├── 05_CUSTODIA/              registro_cadena_custodia.md + RCDC.pdf
└── 06_INFORME_FINAL/         informe_pericial.md  ← documento principal
```

---

## Resumen de hallazgos

Entre el **21 y 23 de abril de 2024**, el usuario `ken` empleó el equipo para **reconocimiento
técnico/OSINT** (Nmap, Parrot Security en VirtualBox, Censys sobre un host con RDP, adaptador WiFi
USB) y para la **recopilación masiva de datos de nómina/personal** de portales gubernamentales,
con **múltiples vectores de exfiltración** (USB, FileZilla FTP, uTorrent, OneDrive) y
**anonimización** (Tor + VPN). Se recuperaron las credenciales (hashes NT) y se documentaron
inconsistencias de la cadena de custodia. Detalle completo en
[`CASO_001/06_INFORME_FINAL/informe_pericial.md`](CASO_001/06_INFORME_FINAL/informe_pericial.md).

## Herramientas utilizadas
FTK Imager 4.7.3.81 · Volatility 3 2.28.0 · Autopsy 4.23.1 · Python 3.13.6 (regipy, pycryptodome).

## Estado
Análisis y redacción del informe **completos**. Pendiente: exportación a PDF y firma del perito.
