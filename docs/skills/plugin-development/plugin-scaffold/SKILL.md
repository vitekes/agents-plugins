---
name: plugin-scaffold
description: Create a new plugin from the repository plugin-template and prepare the initial folder shape, manifest, and implementation entrypoint. Use when starting a new plugin in this repository.
---

# Plugin Scaffold

Use this skill to create a plugin skeleton.

## Read First

- [plugin-template](/C:/Users/vitek/PycharmProjects/agent-plugins/templates/plugin-template)
- [docs/PLUGIN_DEVELOPMENT_GUIDE.md](/C:/Users/vitek/PycharmProjects/agent/docs/PLUGIN_DEVELOPMENT_GUIDE.md)
- [docs/plugin-contract.md](/C:/Users/vitek/PycharmProjects/agent/docs/plugin-contract.md)

## Required Workflow

1. Copy the plugin template into the chosen plugin location.
2. Replace placeholder metadata in `manifest.json`.
3. Confirm resource tier, lifecycle contract, and expected entrypoint.
4. Keep the new plugin isolated from core platform internals.

## Repository-Specific Rules

- Start from `templates/plugin-template`, not from an empty folder.
- Keep plugin structure compatible with `validate_plugin.py`.
