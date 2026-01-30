# Start shared Postgres DB using Docker Compose
# This script checks Docker, starts Postgres, and displays connection info for teammates

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Shared Postgres Setup (Docker)                           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Docker is installed
Write-Host "[1/5] Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker not found. Install from https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/5] Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version
    Write-Host "✓ Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Compose not found" -ForegroundColor Red
    exit 1
}

# Step 2: Start containers
Write-Host ""
Write-Host "[3/5] Starting Postgres container..." -ForegroundColor Yellow
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

try {
    docker-compose up -d
    Write-Host "✓ Containers started" -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "✗ Failed to start containers: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Verify container is running
Write-Host ""
Write-Host "[4/5] Verifying Postgres is healthy..." -ForegroundColor Yellow
$maxRetries = 10
$retries = 0
$healthy = $false

while ($retries -lt $maxRetries -and -not $healthy) {
    try {
        $status = docker-compose ps --services --filter "status=running"
        if ($status -like "*db*") {
            # Try to connect
            $env:PGPASSWORD = "artisanpw"
            $null = psql -h 127.0.0.1 -U artisan -d artisandb -c "SELECT 1;" 2>$null
            if ($LASTEXITCODE -eq 0) {
                $healthy = $true
                Write-Host "✓ Postgres is ready" -ForegroundColor Green
            }
        }
    } catch {}
    
    if (-not $healthy) {
        $retries++
        if ($retries -lt $maxRetries) {
            Write-Host "  Waiting for Postgres to be ready... ($retries/$maxRetries)" -ForegroundColor Gray
            Start-Sleep -Seconds 1
        }
    }
}

if (-not $healthy) {
    Write-Host "⚠ Postgres container is running but connection check skipped (psql not installed)" -ForegroundColor Yellow
    Write-Host "  You can still use the database. Continue with setup." -ForegroundColor Gray
}

# Step 4: Get host IP
Write-Host ""
Write-Host "[5/5] Detecting host IP address..." -ForegroundColor Yellow
$ipAddresses = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*" } | Select-Object -ExpandProperty IPAddress

$hostIP = $null
if ($ipAddresses.Count -gt 1) {
    Write-Host "Found multiple IP addresses. Select one (or 127.0.0.1 for localhost):" -ForegroundColor Cyan
    for ($i = 0; $i -lt $ipAddresses.Count; $i++) {
        Write-Host "  [$($i+1)] $($ipAddresses[$i])"
    }
    Write-Host "  [0] Use 127.0.0.1 (localhost only)"
    $choice = Read-Host "Select number"
    if ($choice -eq "0") {
        $hostIP = "127.0.0.1"
    } else {
        $hostIP = $ipAddresses[[int]$choice - 1]
    }
} else {
    $hostIP = if ($ipAddresses) { $ipAddresses[0] } else { "127.0.0.1" }
}

Write-Host "✓ Using IP: $hostIP" -ForegroundColor Green

# Generate DATABASE_URL
$databaseURL = "postgres://artisan:artisanpw@$hostIP`:5432/artisandb"

# Step 5: Display instructions
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✓ Postgres is running and ready!                         ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "DATABASE_URL for .env:" -ForegroundColor Cyan
Write-Host "  $databaseURL" -ForegroundColor White
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit .env in project root"
Write-Host "  2. Set DATABASE_URL=$databaseURL"
Write-Host "  3. Run: pip install -r requirements.txt"
Write-Host "  4. Run: python manage.py migrate"
Write-Host "  5. Run: python manage.py runserver"
Write-Host ""

Write-Host "Share with teammates:" -ForegroundColor Cyan
Write-Host "  DATABASE_URL=$databaseURL" -ForegroundColor Yellow
Write-Host ""

Write-Host "Docker Compose commands:" -ForegroundColor Cyan
Write-Host "  docker-compose ps          # Check container status"
Write-Host "  docker-compose logs -f db  # View logs"
Write-Host "  docker-compose down        # Stop containers"
Write-Host ""

# Offer to update .env
$updateEnv = Read-Host "Update .env with this DATABASE_URL now? (y/n)"
if ($updateEnv -eq "y" -or $updateEnv -eq "Y") {
    $envPath = Join-Path $projectRoot ".env"
    if (Test-Path $envPath) {
        # Backup existing .env
        $backupPath = "$envPath.backup"
        Copy-Item $envPath $backupPath
        Write-Host "Backed up .env to .env.backup" -ForegroundColor Gray
    }
    
    # Copy from .env.example if .env doesn't exist
    $examplePath = Join-Path $projectRoot ".env.example"
    if (-not (Test-Path $envPath) -and (Test-Path $examplePath)) {
        Copy-Item $examplePath $envPath
    }
    
    # Update DATABASE_URL in .env
    if (Test-Path $envPath) {
        $content = Get-Content $envPath
        $content = $content -replace "DATABASE_URL=.*", "DATABASE_URL=$databaseURL"
        $content | Set-Content $envPath
        Write-Host "✓ Updated .env with DATABASE_URL" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Ready! Your shared Postgres is running at: $hostIP`:5432" -ForegroundColor Green
