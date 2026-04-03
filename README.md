# Agent Plugins

Separate repository for concrete plugin development.

This repository is intended for concrete plugin authoring work that should not modify the main platform repository by default.

## Role

- implement concrete plugin packages;
- keep plugin-specific tests, manifests, packaging, and release assets;
- validate plugin behavior against the contract defined in the main `agent` repository.

## Workspace Model

Expected local layout:

```text
C:\Users\vitek\PycharmProjects\
  agent\
  agent-plugins\
```

The `agent` repository remains the source of truth for:

- plugin contract and governance rules;
- platform-side registry, orchestration, execution, and integration behavior;
- catalog and idea governance decisions.

This repository owns the operational plugin scaffolding template used for day-to-day plugin development:

- `templates/plugin-template`.

For the boundary model between ideas, plugins, modules, and skills, see
[docs/P5_PLUGIN_CATALOG_ARCHITECTURE.md](/C:/Users/vitek/PycharmProjects/agent/docs/P5_PLUGIN_CATALOG_ARCHITECTURE.md)
in the main `agent` repository.

## Repository Structure

```text
docs/            plugin-authoring docs and plugin-development skills
templates/       local plugin scaffolding template
plugins/         concrete plugin implementations
scripts/         local bootstrap and repo maintenance scripts
.github/         CI workflows for plugin validation
```

## Bootstrap

Initialize a new plugin from the local template:

```powershell
.\scripts\new-plugin-from-template.ps1 -PluginId my-new-plugin -PluginName "My New Plugin"
```

Configure the GitHub remote after creating the repository on GitHub:

```powershell
git remote add origin https://github.com/<github-owner>/agent-plugins.git
```

## GitHub Auth

Use `GITHUB_TOKEN` for GitHub API access and HTTPS repository operations.

## Skills

Plugin-development skills used for this repository live in [docs/skills/README.md](/C:/Users/vitek/PycharmProjects/agent-plugins/docs/skills/README.md).
