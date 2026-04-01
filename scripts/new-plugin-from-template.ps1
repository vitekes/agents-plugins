param(
    [Parameter(Mandatory = $true)]
    [string]$PluginId,

    [Parameter(Mandatory = $true)]
    [string]$PluginName
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$templatePath = Join-Path $repoRoot "templates\\plugin-template"
$pluginsRoot = Join-Path $repoRoot "plugins"
$targetPath = Join-Path $pluginsRoot $PluginId

if (-not (Test-Path $templatePath)) {
    throw "plugin-template not found at $templatePath"
}

if (Test-Path $targetPath) {
    throw "Plugin directory already exists: $targetPath"
}

Copy-Item -Recurse -Force $templatePath $targetPath

$manifestPath = Join-Path $targetPath "manifest.json"
if (Test-Path $manifestPath) {
    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
    $manifest.id = $PluginId
    $manifest.name = $PluginName
    $manifest.author = "replace-me"
    $manifest.description = "replace-me"
    $manifest | ConvertTo-Json -Depth 10 | Set-Content $manifestPath
}

Write-Host "Plugin scaffold created at $targetPath"
