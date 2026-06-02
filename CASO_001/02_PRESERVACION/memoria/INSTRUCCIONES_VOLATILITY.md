# Fase 3 — Análisis de memoria volátil con Volatility 3

Indicio: `Laptop Dell/Dump memoria/memdump.mem` (9 GB). Ataca los objetivos
**7 (red), 8 (herramientas), 10 (seguimiento), 11 (exfiltración)** y aporta a 1, 3 y 6.
Sustento: NIST SP 800-86 (análisis de memoria), ISO/IEC 27042 (interpretación).

> **Importante:** se trabaja sobre el `.mem` en **solo lectura**; Volatility no lo modifica.
> Su integridad ya quedó certificada (MD5 a22059f3… PASS, ver Anexo A).

---

## Paso 0 — Instalar Volatility 3

Opción A (rápida, recomendada):
```powershell
pip install volatility3
```
Verifica:
```powershell
vol --help
```
Si `vol` no se reconoce, usa `python -m volatility3.cli` en lugar de `vol` en todos los comandos.

Opción B (desde el repo de GitHub, si prefieres la última versión):
```powershell
git clone https://github.com/volatilityfoundation/volatility3
cd volatility3
pip install -e .
```

> La primera ejecución descarga las *symbol tables* de Windows automáticamente (necesita
> internet). Guarda la **versión** que te imprima `vol --help` o `pip show volatility3`:
> la registramos en la bitácora.

---

## Paso 1 — Variables de ruta (pega esto primero en PowerShell)

```powershell
$IMG = "C:\Users\diego\Desktop\Clases\Forense\Examen Final\Laptop Dell\Dump memoria\memdump.mem"
$OUT = "C:\Users\diego\Desktop\Clases\Forense\Examen Final\CASO_001"
```

---

## Paso 2 — Comandos ordenados (corre y guarda salida)

Corre estos uno por uno. Cada uno guarda su salida en la carpeta correcta. El **primero
es el más importante** (identifica el SO y valida que la imagen es legible):

```powershell
# (1) Identificación del SO y momento del volcado  → obj 1, 3
vol -f $IMG windows.info > "$OUT\02_PRESERVACION\memoria\01_info.txt"

# (2) Procesos en ejecución (lista, árbol y escaneo)  → obj 8, 10
vol -f $IMG windows.pslist  > "$OUT\02_PRESERVACION\procesos\02_pslist.txt"
vol -f $IMG windows.pstree  > "$OUT\02_PRESERVACION\procesos\03_pstree.txt"
vol -f $IMG windows.psscan  > "$OUT\02_PRESERVACION\procesos\04_psscan.txt"

# (3) Líneas de comando de cada proceso  → obj 8, 11 (qué se ejecutó y con qué args)
vol -f $IMG windows.cmdline > "$OUT\02_PRESERVACION\procesos\05_cmdline.txt"

# (4) Conexiones de red  → obj 7, 11 (IPs, puertos, estado)
vol -f $IMG windows.netscan > "$OUT\02_PRESERVACION\red\06_netscan.txt"

# (5) Historial de consola / comandos tecleados  → obj 8, 11
vol -f $IMG windows.cmdscan  > "$OUT\02_PRESERVACION\procesos\07_cmdscan.txt"
vol -f $IMG windows.consoles > "$OUT\02_PRESERVACION\procesos\08_consoles.txt"

# (6) Código inyectado / posible malware  → obj 8, 10
vol -f $IMG windows.malfind > "$OUT\02_PRESERVACION\procesos\09_malfind.txt"

# (7) Hives de registro presentes en RAM  → obj 4, 6
vol -f $IMG windows.registry.hivelist > "$OUT\03_ANALISIS\correlacion\10_hivelist.txt"

# (8) Credenciales en memoria  → obj 6
vol -f $IMG windows.hashdump > "$OUT\03_ANALISIS\correlacion\11_hashdump.txt"
vol -f $IMG windows.lsadump  > "$OUT\03_ANALISIS\correlacion\12_lsadump.txt"

# (9) Archivos referenciados en memoria  → obj 10, 11 (rutas de interés)
vol -f $IMG windows.filescan > "$OUT\03_ANALISIS\13_filescan.txt"
```

---

## Paso 3 — Qué hacer al terminar
1. Pásame primero la salida de **`01_info.txt`** (es corta) para confirmar SO, build y
   fecha del volcado, y validar que la imagen se parsea bien antes de seguir.
2. Conforme tengas las demás, compárteme las que llamen la atención (sobre todo
   `netscan`, `cmdline`, `pstree`); yo:
   - registro cada corrida en la bitácora,
   - extraigo los hallazgos relevantes,
   - los voy redactando en las secciones 7.7–7.11 del informe.

> Si algún plugin tarda mucho o falla, anótalo y seguimos con el resto; lo resolvemos aparte.
