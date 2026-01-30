# Setup developer environment for project
# Run on each developer machine. Copies .env.example -> .env (only if .env not present), creates venv, installs deps

Param(
    [string]$VenvName = ".venv"
)

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path -Path "$root\.env")) {
    Copy-Item -Path "$root\.env.example" -Destination "$root\.env"
    Write-Host "Copied .env.example to .env. Please edit .env to set DATABASE_URL if host isn't 127.0.0.1"
} else {
    Write-Host ".env already exists. Skipping copy."
}

# Create virtualenv
if (-not (Test-Path -Path "$root\$VenvName")) {
    python -m venv $VenvName
    Write-Host "Created virtual environment $VenvName"
} else {
    Write-Host "Virtual environment $VenvName already exists"
}

Write-Host "Activating virtual environment and installing requirements..."
& "$root\$VenvName\Scripts\Activate.ps1"

pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Dependencies installed. To finish: edit .env if needed, then run migrations:\npython manage.py migrate\npython manage.py createsuperuser (optional)\npython manage.py runserver 0.0.0.0:8000"