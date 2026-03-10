$ErrorActionPreference = "Stop"

Set-Location -Path $PSScriptRoot

$pyCmd = $null
$pyArgs = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
  $pyCmd = "py"
  $pyArgs = @("-3")
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  $pyCmd = "python"
} else {
  throw "Python not found. Install Python 3 (or the 'py' launcher) and retry."
}

if (-not (Test-Path ".venv")) {
  & $pyCmd @pyArgs "-m" "venv" ".venv"
}

$venvPy = @(".venv\Scripts\python.exe", ".venv\Scripts\python") | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $venvPy) {
  throw "venv python not found under .venv\Scripts. venv creation may have failed."
}

& $venvPy "-m" "pip" "install" "--upgrade" "pip"
& $venvPy "-m" "pip" "install" "-r" "requirements.txt"

Write-Host "OK: venv ready."

