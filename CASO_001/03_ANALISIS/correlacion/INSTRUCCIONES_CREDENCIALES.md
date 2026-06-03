# Objetivo 6 — Recuperación de credenciales (offline)

El volcado de hashes desde memoria falló ("Hbootkey is not valid"), así que extraemos los
hashes NT **offline** desde los hives **SAM + SYSTEM** (que ya tenemos verificados, 9/9 PASS)
con **impacket secretsdump**. Es la técnica estándar y reproducible.
Sustento: NIST SP 800-86; el método se documenta para defensa técnica.

> Trabaja sobre copias de los hives en solo lectura. secretsdump no los modifica.

## Paso 1 — Instalar impacket
```powershell
pip install impacket
```

## Paso 2 — Extraer hashes locales (SAM + SYSTEM) y secretos LSA (SECURITY)
```powershell
$T = "C:\Users\diego\Desktop\Clases\Forense\Examen Final\Laptop Dell\Triage"
$OUT = "C:\Users\diego\Desktop\Clases\Forense\Examen Final\CASO_001"
$env:PYTHONUTF8 = "1"

secretsdump.py -sam "$T\SAM" -system "$T\system" -security "$T\SECURITY" LOCAL > "$OUT\03_ANALISIS\correlacion\15_secretsdump.txt"
```

> Si `secretsdump.py` no se reconoce, usa:
> ```powershell
> python -m impacket.examples.secretsdump -sam "$T\SAM" -system "$T\system" -security "$T\SECURITY" LOCAL > "$OUT\03_ANALISIS\correlacion\15_secretsdump.txt"
> ```

## Qué obtendremos
- Lista de cuentas locales con su **hash NT** (formato `usuario:rid:lmhash:nthash:::`).
- Secretos LSA y, si existen, credenciales cacheadas (DPAPI system, default password, etc.).

## Después (lo hago yo)
- Registro la corrida en bitácora y documento los hashes en el informe (obj. 6).
- Opcional: intentar **descifrar** el hash de `ken` con diccionario (hashcat/john) — lo
  valoramos según tiempo; la *extracción* ya cumple el objetivo de "recuperar credenciales".
- Los archivos **DPAPI de ken** (`Triage/Users/ken/Protect` y `Crypto`) permiten descifrar
  secretos protegidos (contraseñas guardadas en navegador, etc.) si conseguimos su contraseña
  o la masterkey; queda como línea de análisis posterior.

> Pásame el contenido de `15_secretsdump.txt` cuando termine.
