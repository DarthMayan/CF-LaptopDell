#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor de hashes NT desde los hives SAM + SYSTEM (offline) — Caso Pavana-Hidalgo.

Implementación PURA en Python (regipy + pycryptodome). Se escribió a propósito para no
depender de impacket/secretsdump, que el antivirus del equipo de análisis marca como
hacktool (falso positivo en contexto forense). Reproduce el algoritmo estándar:
bootkey (SysKey) -> hashed bootkey (AES, Win10 1607+) -> hash NT por RID (AES + DES).

Sustento: NIST SP 800-86. No modifica los hives (solo lectura).

Uso: python extraer_hashes_sam.py
"""
import binascii
import struct
import sys
from pathlib import Path

from regipy.registry import RegistryHive
from Crypto.Cipher import AES, DES

ROOT = Path(__file__).resolve().parents[3]
T = ROOT / "Laptop Dell" / "Triage"
SYSTEM = str(T / "system")
SAM = str(T / "SAM")
EMPTY_NT = "31d6cfe0d16ae931b73c59d7e0c089c0"  # hash NT de contraseña vacía


def get_bootkey(system_path):
    h = RegistryHive(system_path)
    cur = next(v.value for v in h.get_key("\\Select").get_values() if v.name == "Current")
    cs = "ControlSet%03d" % cur
    scrambled = ""
    for name in ("JD", "Skew1", "GBG", "Data"):
        k = h.get_key("\\%s\\Control\\Lsa\\%s" % (cs, name))
        scrambled += k.get_class_name()
    scrambled = binascii.unhexlify(scrambled)
    perm = [0x8, 0x5, 0x4, 0x2, 0xB, 0x9, 0xD, 0x3, 0x0, 0x6, 0x1, 0xC, 0xE, 0xA, 0xF, 0x7]
    return bytes(scrambled[perm[i]] for i in range(16)), cur


def decrypt_aes(key, value, iv):
    out = b""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    for i in range(0, len(value), 16):
        block = value[i:i + 16]
        if len(block) < 16:
            block += b"\x00" * (16 - len(block))
        out += cipher.decrypt(block)
    return out


def get_hbootkey(sam_path, bootkey):
    h = RegistryHive(sam_path)
    F = h.get_key("\\SAM\\Domains\\Account").get_value("F")
    # localizar Key0 (primer byte 0x01=RC4 / 0x02=AES) probando offsets conocidos
    for off in (0x68, 0x64, 0x70):
        if F[off] in (1, 2):
            key0 = F[off:]
            break
    else:
        raise RuntimeError("No se localizó SAM_KEY_DATA en F")
    rev = key0[0]
    if rev == 2:  # AES (Windows 10 build 19041)
        data_len = struct.unpack("<L", key0[12:16])[0]
        salt = key0[16:32]
        data = key0[32:32 + data_len]
        return decrypt_aes(bootkey, data, salt)[:16]
    raise RuntimeError("Formato RC4 no esperado en Win10 19041 (rev=%d)" % rev)


def transform_des_key(b7):
    o = [
        b7[0] >> 1,
        ((b7[0] & 0x01) << 6) | (b7[1] >> 2),
        ((b7[1] & 0x03) << 5) | (b7[2] >> 3),
        ((b7[2] & 0x07) << 4) | (b7[3] >> 4),
        ((b7[3] & 0x0F) << 3) | (b7[4] >> 5),
        ((b7[4] & 0x1F) << 2) | (b7[5] >> 6),
        ((b7[5] & 0x3F) << 1) | (b7[6] >> 7),
        b7[6] & 0x7F,
    ]
    return bytes((x << 1) & 0xFF for x in o)


def rid_des_keys(rid):
    k = struct.pack("<L", rid)
    k1 = bytes([k[0], k[1], k[2], k[3], k[0], k[1], k[2]])
    k2 = bytes([k[3], k[0], k[1], k[2], k[3], k[0], k[1]])
    return transform_des_key(k1), transform_des_key(k2)


def decrypt_user_hash(rid, enc16):
    key1, key2 = rid_des_keys(rid)
    d1 = DES.new(key1, DES.MODE_ECB)
    d2 = DES.new(key2, DES.MODE_ECB)
    return d1.decrypt(enc16[:8]) + d2.decrypt(enc16[8:16])


def main():
    bootkey, cs = get_bootkey(SYSTEM)
    print("ControlSet actual : %03d" % cs)
    print("Bootkey (SysKey)  : %s" % binascii.hexlify(bootkey).decode())
    hbootkey = get_hbootkey(SAM, bootkey)
    print("Hashed BootKey    : %s" % binascii.hexlify(hbootkey[:16]).decode())
    print()

    h = RegistryHive(SAM)
    users = h.get_key("\\SAM\\Domains\\Account\\Users")
    rows = []
    for sk in users.iter_subkeys():
        if sk.name == "Names":
            continue
        try:
            rid = int(sk.name, 16)
        except ValueError:
            continue
        V = sk.get_value("V")
        name_off = struct.unpack("<L", V[0x0C:0x10])[0] + 0xCC
        name_len = struct.unpack("<L", V[0x10:0x14])[0]
        username = V[name_off:name_off + name_len].decode("utf-16-le", "replace")

        nt_off = struct.unpack("<L", V[0xA8:0xAC])[0] + 0xCC
        nt_len = struct.unpack("<L", V[0xAC:0xB0])[0]

        blob = V[nt_off:nt_off + nt_len]
        if nt_len < 0x14 or len(blob) < 40:
            nthash = EMPTY_NT  # sin contraseña establecida
        else:
            # SAM_HASH_AES: PekID(2) Rev(2) DataOffset(4) Salt(16) Hash(...)
            salt = blob[8:24]
            enc = blob[24:24 + 16]
            dec_aes = decrypt_aes(hbootkey[:16], enc, salt)[:16]
            nthash = binascii.hexlify(decrypt_user_hash(rid, dec_aes)).decode()
        rows.append((rid, username, nthash))

    rows.sort()
    print("Cuentas locales y hashes NT (formato user:rid:lmhash:nthash:::):")
    print("-" * 78)
    for rid, username, nthash in rows:
        line = "%s:%d:%s:%s:::" % (username, rid, "aad3b435b51404eeaad3b435b51404ee", nthash)
        empty = "  <-- contraseña VACÍA o no establecida" if nthash == EMPTY_NT else ""
        print(line + empty)


if __name__ == "__main__":
    main()
