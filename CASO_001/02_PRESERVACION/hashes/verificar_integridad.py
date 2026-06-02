#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación de integridad de los indicios — Caso 24042024-001-Pavana-Hidalgo.

Calcula MD5, SHA-1 y SHA-256 de cada indicio y los compara contra los valores
documentados en la cadena de custodia / hojas de hashes (.txt). Genera un reporte
con resultado PASS/FAIL por archivo.

Sustento normativo: NIST SP 800-86 (integridad mediante hashing), ISO/IEC 27037
(preservación de evidencia digital). El hashing demuestra que la copia de trabajo
es idéntica a la evidencia recibida y que no hubo alteración.

NOTA sobre la imagen E01: el hash documentado (6ace19ab...) corresponde al CONTENIDO
del disco físico adquirido, NO a los bytes del archivo contenedor .E01. Hashear el
.E01 directamente NO coincidirá. La verificación del E01 se hace con FTK Imager
(Verify Drive/Image) o ewfverify; ver INSTRUCCIONES_HASHING.md. Por eso el .E01 se
excluye de este script.

Uso:
    python verificar_integridad.py
"""

import hashlib
import sys
from datetime import datetime
from pathlib import Path

# Raíz del proyecto: .../Examen Final  (3 niveles arriba de este script)
ROOT = Path(__file__).resolve().parents[3]
EVID = ROOT / "Laptop Dell"
OUT = Path(__file__).resolve().parent / "reporte_integridad.md"

# Valores documentados (MD5 / SHA-1) tomados de los .txt de cadena de custodia.
# Clave = ruta relativa a "Laptop Dell".
REFERENCIA = {
    "Dump memoria/memdump.mem":            ("a22059f3f9c41cc9a2b5e0427a1a6d5e", "7dc3cf3c4a1467c03fee95e85e53eaac2805044b"),
    "Triage/SAM":                          ("155ae6e43137de21cb9747d60dc451d3", "f44f160c339f13d69ac1eedcc05ef0ec3cb0f6e6"),
    "Triage/SECURITY":                     ("8a0b93d74ce72bc98d8b1fb2032488a8", "3e5cd1aa2d1b956b2aa5b6850a0882c29be4b061"),
    "Triage/system":                       ("bcb0e4a82c3dd08d5fc4b9391cb22e26", "f6b736d5c4c2d5c522bf16e837c46dab8ac805bc"),
    "Triage/software":                     ("597f8f124d3e359ce8c663f62c72ed67", "d4f627b13bb249a869cd6545317a3ab7cd94fdcf"),
    "Triage/default":                      ("3e29a18af3b171bb942a60118cbfe57e", "28feccafbdb28fc04267b3daa3f02a4f2b58b8a1"),
    "Triage/Users/ken/NTUSER.DAT":         ("d99efc55c8541eb2b1361b285d9605c3", "9dd806075e583ae960d9585b1b776b16acfb042a"),
    "Triage/Users/ken/UsrClass.dat":       ("b6d3bead582e4f813a8db38540d98e1e", "79a689530e01b48afd4dcab492161db6ee9d1168"),
    "Triage/Users/Default/NTUSER.DAT":     ("ac9dea2283d8bd0f150662e41a871a3d", "c316ef621230655e5bf66ffbfb0899ff9586d663"),
}

CHUNK = 8 * 1024 * 1024  # 8 MiB — necesario para el .mem de 9 GB


def hashes(path: Path):
    md5, sha1, sha256 = hashlib.md5(), hashlib.sha1(), hashlib.sha256()
    total = path.stat().st_size
    leido = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(CHUNK)
            if not b:
                break
            md5.update(b); sha1.update(b); sha256.update(b)
            leido += len(b)
            pct = (leido / total * 100) if total else 100
            print(f"\r  {path.name}: {pct:5.1f}%", end="", file=sys.stderr)
    print("", file=sys.stderr)
    return md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()


def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lineas = [
        "# Reporte de verificación de integridad",
        "",
        f"- **Caso:** 24042024-001-Pavana-Hidalgo",
        f"- **Fecha/hora (local UTC-6):** {ts}",
        f"- **Norma:** NIST SP 800-86 · ISO/IEC 27037",
        f"- **Equipo:** MAYAN (Windows 11)",
        "",
        "| Indicio | Tamaño | MD5 calculado | MD5 doc. | SHA-1 calculado | SHA-256 calculado | Resultado |",
        "|---|---|---|---|---|---|---|",
    ]
    todos_ok = True
    for rel, (md5_doc, sha1_doc) in REFERENCIA.items():
        p = EVID / rel
        if not p.exists():
            lineas.append(f"| `{rel}` | — | — | {md5_doc} | — | — | ⚠️ NO ENCONTRADO |")
            todos_ok = False
            continue
        md5_c, sha1_c, sha256_c = hashes(p)
        ok = (md5_c == md5_doc.lower()) and (sha1_c == sha1_doc.lower())
        todos_ok = todos_ok and ok
        estado = "✅ PASS" if ok else "❌ FAIL"
        size = f"{p.stat().st_size:,}"
        lineas.append(
            f"| `{rel}` | {size} | {md5_c} | {md5_doc} | {sha1_c} | {sha256_c} | {estado} |"
        )

    lineas += [
        "",
        f"**Resultado global:** {'✅ TODOS LOS INDICIOS ÍNTEGROS' if todos_ok else '❌ HAY DISCREPANCIAS — revisar'}",
        "",
        "> La imagen `001-003-LAptop-Pavana T3.E01` se verifica aparte con FTK Imager",
        "> (Verify Drive/Image), ya que su hash documentado es del contenido del disco,",
        "> no del archivo contenedor. Ver INSTRUCCIONES_HASHING.md.",
    ]
    OUT.write_text("\n".join(lineas), encoding="utf-8")
    print("\n".join(lineas))
    print(f"\n>>> Reporte guardado en: {OUT}")


if __name__ == "__main__":
    main()
