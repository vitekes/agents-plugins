---
name: plugin-lifecycle-implement
description: Implement plugin lifecycle behavior including init, activate, deactivate, shutdown, and health handling in a plugin built from this repository template. Use when adding or changing actual plugin runtime logic.
---

# Plugin Lifecycle Implement

Use this skill to implement plugin runtime behavior.

## Read First

- [plugin-template/src/main.py](/C:/Users/vitek/PycharmProjects/agent-plugins/templates/plugin-template/src/main.py)
- [docs/plugin-contract.md](/C:/Users/vitek/PycharmProjects/agent/docs/plugin-contract.md)
- [docs/PLUGIN_DEVELOPMENT_GUIDE.md](/C:/Users/vitek/PycharmProjects/agent/docs/PLUGIN_DEVELOPMENT_GUIDE.md)

## Required Workflow

1. Implement lifecycle handlers against the plugin contract.
2. Keep activation and health behavior deterministic and fast.
3. Keep shutdown and deactivation behavior safe and idempotent.
4. Add or update plugin tests for lifecycle behavior.

## Repository-Specific Rules

- Do not bypass the template lifecycle interface.
- Do not introduce forbidden execution patterns listed in governance docs.
