<#
.SYNOPSIS
    Tears down and recreates the local Docker Compose database.
    WARNING: destroys all data.
#>
$compose = Join-Path $PSScriptRoot ".." "docker" "docker-compose.yml"
Write-Warning "This will delete all data in the local dev database."
$confirm = Read-Host "Type YES to continue"
if ($confirm -ne "YES") { Write-Host "Aborted."; exit 0 }

docker compose -f $compose down -v
docker compose -f $compose up -d
Write-Host "Database reset complete. Waiting for health..." -ForegroundColor Green
Start-Sleep -Seconds 5
