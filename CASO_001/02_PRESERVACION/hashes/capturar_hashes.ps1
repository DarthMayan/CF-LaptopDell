<#
.SYNOPSIS
    Recalcula los hashes de los indicios EN VIVO, los muestra en consola comparados
    contra los valores documentados, y toma una captura de pantalla automática como
    evidencia (04_EVIDENCIA/capturas/).

.DESCRIPTION
    Caso 24042024-001-Pavana-Hidalgo. Sustento: NIST SP 800-86 (hashing de integridad),
    ISO/IEC 27037. La captura sirve de respaldo visual auditable del resultado.

.PARAMETER SkipMem
    Omite el volcado de memoria (9 GB) para una captura rápida solo de los hives.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\capturar_hashes.ps1
    powershell -ExecutionPolicy Bypass -File .\capturar_hashes.ps1 -SkipMem
#>
param([switch]$SkipMem)

$ErrorActionPreference = "Stop"

# --- Rutas ---
$ROOT = (Resolve-Path "$PSScriptRoot\..\..\..").Path
$EVID = Join-Path $ROOT "Laptop Dell"
$CAP  = Join-Path $ROOT "CASO_001\04_EVIDENCIA\capturas"
if (-not (Test-Path $CAP)) { New-Item -ItemType Directory -Path $CAP -Force | Out-Null }

# --- Valores documentados (MD5 / SHA-1) ---
$REF = [ordered]@{
    "Dump memoria\memdump.mem"        = @("a22059f3f9c41cc9a2b5e0427a1a6d5e","7dc3cf3c4a1467c03fee95e85e53eaac2805044b")
    "Triage\SAM"                      = @("155ae6e43137de21cb9747d60dc451d3","f44f160c339f13d69ac1eedcc05ef0ec3cb0f6e6")
    "Triage\SECURITY"                 = @("8a0b93d74ce72bc98d8b1fb2032488a8","3e5cd1aa2d1b956b2aa5b6850a0882c29be4b061")
    "Triage\system"                   = @("bcb0e4a82c3dd08d5fc4b9391cb22e26","f6b736d5c4c2d5c522bf16e837c46dab8ac805bc")
    "Triage\software"                 = @("597f8f124d3e359ce8c663f62c72ed67","d4f627b13bb249a869cd6545317a3ab7cd94fdcf")
    "Triage\default"                  = @("3e29a18af3b171bb942a60118cbfe57e","28feccafbdb28fc04267b3daa3f02a4f2b58b8a1")
    "Triage\Users\ken\NTUSER.DAT"     = @("d99efc55c8541eb2b1361b285d9605c3","9dd806075e583ae960d9585b1b776b16acfb042a")
    "Triage\Users\ken\UsrClass.dat"   = @("b6d3bead582e4f813a8db38540d98e1e","79a689530e01b48afd4dcab492161db6ee9d1168")
    "Triage\Users\Default\NTUSER.DAT" = @("ac9dea2283d8bd0f150662e41a871a3d","c316ef621230655e5bf66ffbfb0899ff9586d663")
}

Clear-Host
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " VERIFICACION DE INTEGRIDAD - Caso 24042024-001-Pavana-Hidalgo"            -ForegroundColor Cyan
Write-Host " Norma: NIST SP 800-86 / ISO-IEC 27037   |   Equipo: MAYAN (Windows 11)"   -ForegroundColor Cyan
Write-Host " Fecha/hora: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') (UTC-6)"            -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""

$global_ok = $true
foreach ($rel in $REF.Keys) {
    if ($SkipMem -and $rel -like "*memdump.mem") {
        Write-Host ("{0,-34} OMITIDO (-SkipMem)" -f $rel) -ForegroundColor DarkGray
        continue
    }
    $path = Join-Path $EVID $rel
    if (-not (Test-Path $path)) {
        Write-Host ("{0,-34} NO ENCONTRADO" -f $rel) -ForegroundColor Yellow
        $global_ok = $false
        continue
    }
    Write-Host ("Calculando: {0} ..." -f $rel) -ForegroundColor DarkGray
    $md5  = (Get-FileHash -Algorithm MD5    -Path $path).Hash.ToLower()
    $sha1 = (Get-FileHash -Algorithm SHA1   -Path $path).Hash.ToLower()
    $sha256 = (Get-FileHash -Algorithm SHA256 -Path $path).Hash.ToLower()
    $md5_ok  = ($md5  -eq $REF[$rel][0])
    $sha1_ok = ($sha1 -eq $REF[$rel][1])
    $ok = $md5_ok -and $sha1_ok
    $global_ok = $global_ok -and $ok
    $estado = if ($ok) { "PASS" } else { "FAIL" }
    $color  = if ($ok) { "Green" } else { "Red" }
    Write-Host ("  Indicio : {0}" -f $rel)
    Write-Host ("  MD5     : {0}   [{1}]" -f $md5,  $(if($md5_ok){"OK"}else{"DIF"}))
    Write-Host ("  SHA-1   : {0}   [{1}]" -f $sha1, $(if($sha1_ok){"OK"}else{"DIF"}))
    Write-Host ("  SHA-256 : {0}" -f $sha256)
    Write-Host ("  RESULTADO: {0}" -f $estado) -ForegroundColor $color
    Write-Host ""
}

Write-Host "--------------------------------------------------------------------------"
$msg = if ($global_ok) { " RESULTADO GLOBAL: TODOS LOS INDICIOS INTEGROS (PASS)" } else { " RESULTADO GLOBAL: HAY DISCREPANCIAS - REVISAR" }
Write-Host $msg -ForegroundColor $(if($global_ok){"Green"}else{"Red"})
Write-Host " Imagen E01: se verifica aparte con FTK Imager (Verify Drive/Image)." -ForegroundColor DarkGray
Write-Host "--------------------------------------------------------------------------"
Write-Host ""

# --- Captura de pantalla automatica ---
Start-Sleep -Milliseconds 800   # deja renderizar la consola antes de capturar
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$b   = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap($b.Width, $b.Height)
$g   = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$file  = Join-Path $CAP "hashes_integridad_$stamp.png"
$bmp.Save($file, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Host ("Captura guardada en: {0}" -f $file) -ForegroundColor Cyan
