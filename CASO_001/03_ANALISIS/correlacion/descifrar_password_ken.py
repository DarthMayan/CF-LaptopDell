#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ataque de diccionario al hash NT de 'ken' (obj. 6, profundización).
NT = MD4(password.encode('utf-16-le')). Objetivo: f12c418083c05e3a7de78582e61f652d.

Diccionario temático (común + español + pentesting + anime, por el perfil observado) con
mutaciones (mayúsculas, leet, sufijos/prefijos). Reproducible. Si falla, usar hashcat -m 1000
con rockyou + reglas best64.
"""
from Crypto.Hash import MD4

TARGET = "f12c418083c05e3a7de78582e61f652d"

def nt(p):
    return MD4.new(p.encode("utf-16-le")).hexdigest()

base = [
    # comunes
    "password","contraseña","contrasena","admin","administrador","root","toor","welcome",
    "bienvenido","qwerty","asdf","asdfgh","zxcvbn","123qwe","qwerty123","letmein","secret",
    "secreto","changeme","cambiame","master","login","user","usuario","windows","microsoft",
    # nombre / caso
    "ken","kenneth","kenny","pavana","hidalgo","pavanahidalgo","nomina","nominas","forense",
    "fiscalia","laptop","dell",
    # pentest / tech
    "kali","parrot","linux","hacker","hack","nmap","tor","vpn","censys","osint","metasploit",
    "anonymous","anon","pentest","exploit","shell","payload","ubuntu","server","filezilla",
    # anime (perfil observado)
    "anime","otaku","naruto","sasuke","goku","vegeta","luffy","zoro","ichigo","saitama","eren",
    "mikasa","tanjiro","gojo","sukuna","itachi","kakashi","dragonball","onepiece","bleach",
    "waifu","senpai","kawaii","manga",
    # deportivo/varios
    "futbol","mexico","chivas","america","barcelona","realmadrid","dragon","monkey","superman",
]

suffix = ["","1","12","123","1234","12345","123456","!","1!","12!","123!","01","07","00",
          "2019","2020","2021","2022","2023","2024","2025","2024!","#","*",".","$","_","69","007"]
prefix = ["","!","@","#","1"]

def leet(w):
    t = str.maketrans({"a":"4","e":"3","i":"1","o":"0","s":"5","t":"7"})
    return w.translate(t)

def variants(w):
    out = set()
    for form in {w, w.lower(), w.upper(), w.capitalize(), leet(w), leet(w).capitalize()}:
        for pre in prefix:
            for suf in suffix:
                out.add(pre + form + suf)
    return out

cands = set()
for w in base:
    cands |= variants(w)
# combinaciones de dos palabras temáticas frecuentes
for a in ["ken","anime","kali","tor","naruto","goku","hidalgo","pavana"]:
    for b in ["2024","123","!","mexico","hacker","ken"]:
        cands.add(a + b); cands.add((a+b).capitalize()); cands.add(a + "_" + b)

found = None
for c in cands:
    if nt(c) == TARGET:
        found = c
        break

print(f"Candidatos probados: {len(cands):,}")
print("RESULTADO:", f"CONTRASEÑA = '{found}'" if found else "no encontrada en este diccionario")
