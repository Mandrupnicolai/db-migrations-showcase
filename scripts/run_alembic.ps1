<#
.SYNOPSIS
    Runs Alembic migrations against the configured PostgreSQL instance.
.PARAMETER Target
    Alembic revision target. Defaults to 'head'.
#>
param(
    [string]$Target = "head"
)

$envFile = Join-Path $PSScriptRoot ".." ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.+)$') {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}

if (-not $env:DATABASE_URL) {
    Write-Error "DATABASE_URL environment variable is not set. Copy .env.example to .env and fill in values."
    exit 1
}

$root = Join-Path $PSScriptRoot ".."
Push-Location $root
try {
    Write-Host "Running Alembic upgrade to: $Target" -ForegroundColor Cyan
    python -m alembic -c alembic/alembic.ini upgrade $Target
} finally {
    Pop-Location
}
