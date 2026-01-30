# Start shared Postgres DB using docker-compose
# Run this on the host machine that will serve as the shared DB

Set-Location -Path (Split-Path -Parent $PSScriptRoot)

Write-Host "Starting Postgres container via docker-compose..."
docker-compose up -d db

Start-Sleep -Seconds 3

Write-Host "Container status:"
docker-compose ps db

Write-Host "Postgres will be available on port 5432 of the host.\nEdit .env to point DATABASE_URL to the host IP if needed."