<#
.SYNOPSIS
    Runs Flyway migrations against the configured PostgreSQL instance.
.PARAMETER Command
    Flyway command to execute. Defaults to 'migrate'.
#>
param(
    [string]$Command = "migrate"
)

$envFile = Join-Path $PSScriptRoot ".." ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.+)$') {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}

$required = @("POSTGRES_HOST","POSTGRES_PORT","POSTGRES_DB","POSTGRES_USER","POSTGRES_PASSWORD")
foreach ($var in $required) {
    if (-not (Get-Item "Env:$var" -ErrorAction SilentlyContinue)) {
        Write-Error "$var is not set. Copy .env.example to .env and fill in values."
        exit 1
    }
}

$env:FLYWAY_URL      = "jdbc:postgresql://${env:POSTGRES_HOST}:${env:POSTGRES_PORT}/${env:POSTGRES_DB}"
$env:FLYWAY_USER     = $env:POSTGRES_USER
$env:FLYWAY_PASSWORD = $env:POSTGRES_PASSWORD

$root = Join-Path $PSScriptRoot ".." "flyway"
Push-Location $root
try {
    Write-Host "Running Flyway $Command ..." -ForegroundColor Cyan
    flyway -configFiles="conf/flyway.toml" $Command
} finally {
    Pop-Location
}
