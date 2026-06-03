#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enumera todas las cuentas del SAM y detecta cuentas ocultas (obj. 4/10/12)."""
from pathlib import Path
from regipy.registry import RegistryHive

ROOT = Path(__file__).resolve().parents[3]
T = ROOT / "Laptop Dell" / "Triage"

print("=== SAM: cuentas en \\SAM\\Domains\\Account\\Users\\Names ===")
sam = RegistryHive(str(T / "SAM"))
names = sam.get_key(r"\SAM\Domains\Account\Users\Names")
for sk in names.iter_subkeys():
    print("  usuario:", repr(sk.name))

print("\n=== SAM: RIDs presentes en \\SAM\\Domains\\Account\\Users ===")
users = sam.get_key(r"\SAM\Domains\Account\Users")
for sk in users.iter_subkeys():
    if sk.name != "Names":
        print("  RID:", sk.name, "->", int(sk.name, 16))

print("\n=== SOFTWARE: Winlogon\\SpecialAccounts\\UserList (cuentas OCULTAS del login) ===")
sw = RegistryHive(str(T / "software"))
try:
    ul = sw.get_key(r"\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList")
    vals = list(ul.get_values())
    if not vals:
        print("  (la clave existe pero no tiene valores)")
    for v in vals:
        print("  ", v.name, "=", v.value, "  <-- 0 = OCULTA del inicio de sesión")
except Exception as e:
    print("  No existe la clave SpecialAccounts\\UserList ->", type(e).__name__)
