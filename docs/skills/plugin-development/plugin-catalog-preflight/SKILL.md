---
name: plugin-catalog-preflight
description: Run the required preflight checks before creating or changing a plugin, including duplicate search, standards review, forbidden-pattern review, and plugin constraint review. Use before any plugin implementation work in this repository.
---

# Plugin Catalog Preflight

Use this skill before starting plugin work.

## Read First

- [docs/AGENT_CONSTRAINTS.md](/C:/Users/vitek/PycharmProjects/agent/docs/AGENT_CONSTRAINTS.md)
- [docs/IDEA_CATALOG_GUIDE.md](/C:/Users/vitek/PycharmProjects/agent/docs/IDEA_CATALOG_GUIDE.md)
- [docs/plugin-contract.md](/C:/Users/vitek/PycharmProjects/agent/docs/plugin-contract.md)
- [docs/PLUGIN_DEVELOPMENT_GUIDE.md](/C:/Users/vitek/PycharmProjects/agent/docs/PLUGIN_DEVELOPMENT_GUIDE.md)
- [docs/P5_PLUGIN_CATALOG_ARCHITECTURE.md](/C:/Users/vitek/PycharmProjects/agent/docs/P5_PLUGIN_CATALOG_ARCHITECTURE.md)

## Required Output

- confirm whether similar idea or plugin already exists;
- confirm applicable standards and forbidden patterns;
- confirm whether the task is truly plugin work and not a core platform change;
- confirm approval and lifecycle prerequisites relevant to the plugin path;
- confirm that plugin-package work is not being confused with catalog governance or platform module lifecycle work.

## Repository-Specific Rules

- Do not start plugin implementation before duplicate and standards checks.
- If the requested change actually belongs in the core plugin system, switch to platform-development skills in `agent` and record the boundary decision.
