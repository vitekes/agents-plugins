param(
    [Parameter(Mandatory = $true)]
    [string]$GithubOwner
)

$ErrorActionPreference = "Stop"

$remoteUrl = "https://github.com/$GithubOwner/agents-plugins.git"

git remote remove origin 2>$null
git remote add origin $remoteUrl

Write-Host "Configured origin -> $remoteUrl"
