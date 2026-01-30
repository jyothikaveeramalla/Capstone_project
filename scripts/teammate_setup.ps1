# Setup for teammate to connect to shared Docker Postgres
# Run this on each developer machine to connect to the shared database

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Teammate Setup: Connect to Shared Postgres               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Get DATABASE_URL from user
Write-Host "Paste the DATABASE_URL shared by your team lead:" -ForegroundColor Yellow
$databaseURL = Read-Host "DATABASE_URL"

if (-not $databaseURL -or -not $databaseURL.StartsWith("postgres://")) {
    Write-Host "✗ Invalid DATABASE_URL format" -ForegroundColor Red
    exit 1
}

Write-Host "✓ DATABASE_URL received" -ForegroundColor Green
Write-Host ""

# Setup project root
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

# Create .env
Write-Host "[1/4] Creating .env..." -ForegroundColor Yellow
$envPath = Join-Path $projectRoot ".env"

if (Test-Path $envPath) {
    Write-Host "  .env already exists, updating..." -ForegroundColor Gray
} else {
    # Copy from example
    $examplePath = Join-Path $projectRoot ".env.example"
    if (Test-Path $examplePath) {
        Copy-Item $examplePath $envPath
        Write-Host "  Copied from .env.example" -ForegroundColor Gray
    }
}

# Update DATABASE_URL
$content = if (Test-Path $envPath) { Get-Content $envPath } else { "" }
if ($content -match "DATABASE_URL=") {
    $content = $content -replace "DATABASE_URL=.*", "DATABASE_URL=$databaseURL"
} else {
    $content += "`nDATABASE_URL=$databaseURL"
}
$content | Set-Content $envPath
Write-Host "✓ .env configured" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "[2/4] Creating Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path ".\.venv")) {
    python -m venv .venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "  Virtual environment already exists" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"
pip install -q --upgrade pip
pip install -q -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Run migrations
Write-Host "[4/4] Running migrations..." -ForegroundColor Yellow
python manage.py migrate
Write-Host "✓ Migrations completed" -ForegroundColor Green
Write-Host ""

# Verify connection
Write-Host "Verifying database connection..." -ForegroundColor Yellow
python scripts/verify_shared_db.py
Write-Host ""

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✓ Setup complete! Ready to use shared database.         ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "Start the development server:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""

Write-Host "Test shared visibility:" -ForegroundColor Cyan
Write-Host "  - Ask team lead to add a product" -ForegroundColor Gray
Write-Host "  - Refresh your product list" -ForegroundColor Gray
Write-Host "  - Product should appear (same database)" -ForegroundColor Gray
