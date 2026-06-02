# Fase 1 — Verificación de integridad (PASOS A EJECUTAR)

Objetivo pericial #9: *verificar y certificar la integridad de los elementos probatorios,
indicando el método de validación (hashing) y la norma en que se sustenta.*
Sustento: **NIST SP 800-86** (hashing para integridad) y **ISO/IEC 27037** (preservación).

Hay dos verificaciones, porque hay dos tipos de evidencia:

---

## A) Indicios "crudos" (.mem y hives de registro) → script de Python

Estos archivos se verifican hasheando sus bytes directamente y comparando contra los
valores documentados en los `.txt` de cadena de custodia.

**Pasos:**
1. Abre PowerShell en la carpeta del caso.
2. Ejecuta:
   ```powershell
   cd "C:\Users\diego\Desktop\Clases\Forense\Examen Final\CASO_001\02_PRESERVACION\hashes"
   python verificar_integridad.py
   ```
3. El script calcula MD5 / SHA-1 / SHA-256 de cada indicio, los compara con los
   documentados y genera **`reporte_integridad.md`** con PASS/FAIL.
   - El `.mem` (9 GB) tarda unos minutos; muestra el % de avance.
4. Cuando termine, avísame y registramos el resultado en la bitácora + lo pegamos
   en el informe (Anexo de hashes).

> Resultado esperado: **PASS** en todos. Si algo da **FAIL**, NO se sigue analizando ese
> indicio hasta esclarecer la discrepancia (se documenta como incidencia).

---

## B) Imagen de disco `001-003-LAptop-Pavana T3.E01` (40 GB) → FTK Imager

⚠️ **No** se hashea el archivo `.E01` con el script: el hash documentado
(`MD5 6ace19abd1a8d25589be07d68e9a7bcc`) es del **contenido del disco físico**, no del
contenedor `.E01`. Se verifica con la función nativa de FTK Imager (que ya tienes):

**Pasos en FTK Imager:**
1. `File → Add Evidence Item → Image File` → selecciona `001-003-LAptop-Pavana T3.E01`.
2. En el árbol, clic derecho sobre la evidencia → **`Verify Drive/Image`**.
3. FTK recalcula MD5 y SHA-1 del contenido y los compara con los almacenados en el `.E01`.
4. Al terminar muestra "Verification Results": **Computed vs Stored / Report Hash**.
   - Debe coincidir con **MD5 `6ace19abd1a8d25589be07d68e9a7bcc`** y
     **SHA-1 `3b401352e1b6b60f73dd30dce97f12c85a2adae7`**.
5. **Captura de pantalla** de la ventana de resultados → guárdala en
   `CASO_001/04_EVIDENCIA/capturas/` con nombre `verify_E01_ftk.png`.
6. Avísame y registramos en bitácora.

---

## Qué entrego yo cuando me pases los resultados
- Redacto la entrada de bitácora (actividad #003).
- Relleno la sección de integridad del informe + tabla del Anexo de hashes.
- Marco el objetivo #9 como cubierto.
