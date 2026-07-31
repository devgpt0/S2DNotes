[CmdletBinding()]
param(
    [switch]$KeepRunning
)

$ErrorActionPreference = "Stop"
$projectDirectory = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$previousDirectory = Get-Location
$started = $false

Set-Location -LiteralPath $projectDirectory
try {
    docker compose --env-file .env.example up --build --detach
    $started = $true

    $deadline = (Get-Date).AddMinutes(15)
    $health = $null
    while ((Get-Date) -lt $deadline) {
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 10
            if ($health.index_state -eq "indexed") {
                break
            }
        } catch {
            $health = $null
        }
        Start-Sleep -Seconds 5
    }

    if ($null -eq $health -or $health.index_state -ne "indexed") {
        throw "RAG startup indexing did not complete within 15 minutes."
    }

    $tree = Invoke-RestMethod -Uri "http://localhost:8000/tree" -TimeoutSec 30
    if ($tree.files.Count -lt 1) {
        throw "RAG startup completed without indexed Markdown files."
    }

    $retrievalBody = @{ query = "learning"; limit = 3; backend = "local" } |
        ConvertTo-Json -Compress
    $retrieval = Invoke-RestMethod `
        -Method Post `
        -Uri "http://localhost:8000/retrieve" `
        -ContentType "application/json" `
        -Body $retrievalBody `
        -TimeoutSec 60
    if ($null -eq $retrieval.citations) {
        throw "Local RAG retrieval did not return a citations array."
    }

    Write-Output "Compose smoke test passed: $($tree.files.Count) Markdown files indexed."
} finally {
    try {
        if ($started -and -not $KeepRunning) {
            docker compose --env-file .env.example down
        }
    } finally {
        Set-Location -LiteralPath $previousDirectory
    }
}
