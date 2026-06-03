#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descifrado DPAPI de contraseñas guardadas en navegadores (Brave/Edge) — obj. 6/11.

Flujo: masterkey DPAPI de 'ken' (con su contraseña + SID) -> clave AES del navegador
(en 'Local State') -> contraseñas del 'Login Data' (AES-256-GCM, esquema v10).
Reproducible. Requiere: dpapick3, pycryptodome.
"""
import base64
import json
import os
import sqlite3
import sys
from pathlib import Path

from dpapick3 import masterkey, blob
from Crypto.Cipher import AES

ROOT = Path(__file__).resolve().parents[3]
PROTECT = ROOT / "Laptop Dell" / "Triage" / "Users" / "ken" / "Protect" / "S-1-5-21-1936453629-2262114833-2442330573-1001"
DPAPI_DIR = ROOT / "CASO_001" / "03_ANALISIS" / "autopsy_export" / "dpapi"
SID = "S-1-5-21-1936453629-2262114833-2442330573-1001"
PASSWORD = "MyPassword"

BROWSERS = {
    "Brave": (DPAPI_DIR / "brave_Local_State" / "Brave-Browser" / "User Data" / "Local State",
              DPAPI_DIR / "brave_Local_State" / "Brave-Browser" / "User Data" / "Default" / "Login Data"),
    "Edge":  (DPAPI_DIR / "edge_Local_State" / "User Data" / "Local State",
              DPAPI_DIR / "edge_Local_State" / "User Data" / "Default" / "Login Data"),
}


def cargar_masterkeys():
    mkp = masterkey.MasterKeyPool()
    mkp.loadDirectory(str(PROTECT))
    n = mkp.try_credential(SID, PASSWORD)
    print(f"[*] Masterkeys descifradas con la contraseña: {n}")
    return mkp


def aes_key_navegador(mkp, local_state_path):
    data = json.loads(Path(local_state_path).read_text(encoding="utf-8"))
    enc_key = base64.b64decode(data["os_crypt"]["encrypted_key"])
    assert enc_key[:5] == b"DPAPI", "no es blob DPAPI"
    bl = blob.DPAPIBlob(enc_key[5:])
    mks = mkp.getMasterKeys(bl.mkguid.encode())
    for mk in mks:
        if mk.decrypted:
            bl.decrypt(mk.get_key())
            if bl.decrypted:
                return bl.cleartext
    raise RuntimeError("no se pudo descifrar la clave AES (masterkey no disponible/contraseña)")


def descifrar_v10(blob_pwd, aes_key):
    # v10: 'v10' + nonce(12) + ciphertext + tag(16)
    if blob_pwd[:3] not in (b"v10", b"v11"):
        return "(no v10/v11 — DPAPI directo o vacío)"
    nonce = blob_pwd[3:15]
    ct = blob_pwd[15:-16]
    tag = blob_pwd[-16:]
    try:
        c = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        return c.decrypt_and_verify(ct, tag).decode("utf-8", "replace")
    except Exception as e:
        return f"(error: {e})"


def main():
    mkp = cargar_masterkeys()
    out = []
    for navegador, (ls, ld) in BROWSERS.items():
        out.append("\n" + "=" * 70 + f"\n {navegador}\n" + "=" * 70)
        if not ls.exists() or not ld.exists():
            out.append(f"  [!] Falta Local State o Login Data ({ls.exists()=}, {ld.exists()=})")
            continue
        try:
            key = aes_key_navegador(mkp, ls)
            out.append(f"  Clave AES del navegador obtenida ({len(key)} bytes).")
        except Exception as e:
            out.append(f"  [!] {e}")
            continue
        # copiar la BD para no bloquear y leer
        con = sqlite3.connect(str(ld))
        try:
            rows = con.execute(
                "SELECT origin_url, username_value, password_value FROM logins"
            ).fetchall()
        except Exception as e:
            out.append(f"  [!] no se pudo leer logins: {e}")
            con.close(); continue
        con.close()
        out.append(f"  Credenciales encontradas: {len(rows)}")
        for url, user, pwd in rows:
            clear = descifrar_v10(pwd, key) if pwd else "(vacío)"
            out.append(f"    - URL: {url}\n      usuario: {user}\n      password: {clear}")
    texto = "\n".join(out)
    print(texto)
    (Path(__file__).resolve().parent / "16_credenciales_navegador.txt").write_text(texto, encoding="utf-8")


if __name__ == "__main__":
    main()
