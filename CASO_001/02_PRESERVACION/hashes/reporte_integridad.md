# Reporte de verificación de integridad

- **Caso:** 24042024-001-Pavana-Hidalgo
- **Fecha/hora (local UTC-6):** 2026-06-02 16:45:00
- **Norma:** NIST SP 800-86 · ISO/IEC 27037
- **Equipo:** MAYAN (Windows 11)

| Indicio | Tamaño | MD5 calculado | MD5 doc. | SHA-1 calculado | SHA-256 calculado | Resultado |
|---|---|---|---|---|---|---|
| `Dump memoria/memdump.mem` | 9,640,603,648 | a22059f3f9c41cc9a2b5e0427a1a6d5e | a22059f3f9c41cc9a2b5e0427a1a6d5e | 7dc3cf3c4a1467c03fee95e85e53eaac2805044b | 632acb2c8f4f0774152a214779aac7f9228677cf98387a3aca196b83ef31c500 | ✅ PASS |
| `Triage/SAM` | 65,536 | 155ae6e43137de21cb9747d60dc451d3 | 155ae6e43137de21cb9747d60dc451d3 | f44f160c339f13d69ac1eedcc05ef0ec3cb0f6e6 | 0913abb4b03afac189e389b8f89405a7cc735c8600b6abeea65e2f0020dbd746 | ✅ PASS |
| `Triage/SECURITY` | 65,536 | 8a0b93d74ce72bc98d8b1fb2032488a8 | 8a0b93d74ce72bc98d8b1fb2032488a8 | 3e5cd1aa2d1b956b2aa5b6850a0882c29be4b061 | 8961e47133ed85d021dadb2bcc903a3fe427330516321c152dbdc80f8f134bc0 | ✅ PASS |
| `Triage/system` | 14,417,920 | bcb0e4a82c3dd08d5fc4b9391cb22e26 | bcb0e4a82c3dd08d5fc4b9391cb22e26 | f6b736d5c4c2d5c522bf16e837c46dab8ac805bc | c9b80d44eb45317c5947c7f457ac8f0d8ad6f84a873c1cef1f4ecd985b1f74ca | ✅ PASS |
| `Triage/software` | 78,905,344 | 597f8f124d3e359ce8c663f62c72ed67 | 597f8f124d3e359ce8c663f62c72ed67 | d4f627b13bb249a869cd6545317a3ab7cd94fdcf | 875296cc990c40131f56fc73d72dca032236e91312866939c9af89b1148fe922 | ✅ PASS |
| `Triage/default` | 524,288 | 3e29a18af3b171bb942a60118cbfe57e | 3e29a18af3b171bb942a60118cbfe57e | 28feccafbdb28fc04267b3daa3f02a4f2b58b8a1 | 5e257dd8d1d0162bd95aa5a80376879e737939d51c9eed0e9d4159585b7c6cfb | ✅ PASS |
| `Triage/Users/ken/NTUSER.DAT` | 1,572,864 | d99efc55c8541eb2b1361b285d9605c3 | d99efc55c8541eb2b1361b285d9605c3 | 9dd806075e583ae960d9585b1b776b16acfb042a | 61623bab0e26da8ad1b9f36e1ea03e935f044420a92339ce41eec499419d3569 | ✅ PASS |
| `Triage/Users/ken/UsrClass.dat` | 3,932,160 | b6d3bead582e4f813a8db38540d98e1e | b6d3bead582e4f813a8db38540d98e1e | 79a689530e01b48afd4dcab492161db6ee9d1168 | a582958e7d3dabe8ab15786c823eb789837dafb92783f8204be72bffb27b78da | ✅ PASS |
| `Triage/Users/Default/NTUSER.DAT` | 262,144 | ac9dea2283d8bd0f150662e41a871a3d | ac9dea2283d8bd0f150662e41a871a3d | c316ef621230655e5bf66ffbfb0899ff9586d663 | af786bd06f9224c1e34abea5cbfdcae1e93731e47df8a2b42d0c8c488b3175eb | ✅ PASS |

**Resultado global:** ✅ TODOS LOS INDICIOS ÍNTEGROS

> La imagen `001-003-LAptop-Pavana T3.E01` se verifica aparte con FTK Imager
> (Verify Drive/Image), ya que su hash documentado es del contenido del disco,
> no del archivo contenedor. Ver INSTRUCCIONES_HASHING.md.