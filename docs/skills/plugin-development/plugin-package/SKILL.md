---
name: plugin-package
description: Prepare plugin packaging artifacts including Docker image inputs and repository packaging readiness. Use when plugin work is moving from implementation to distributable artifact preparation.
---

# Plugin Package

Use this skill for plugin packaging readiness.

## Read First

- [plugin-template/Dockerfile](/C:/Users/vitek/PycharmProjects/agent-plugins/templates/plugin-template/Dockerfile)
- [plugin-template/requirements.txt](/C:/Users/vitek/PycharmProjects/agent-plugins/templates/plugin-template/requirements.txt)
- [docs/PLUGIN_DEVELOPMENT_GUIDE.md](/C:/Users/vitek/PycharmProjects/agent/docs/PLUGIN_DEVELOPMENT_GUIDE.md)

## Required Workflow

1. Verify manifest, code, tests, and Dockerfile readiness.
2. Confirm packaging inputs match the implemented plugin.
3. Report whether the plugin is packaging-ready or what is still missing.

## Repository-Specific Rules

- Packaging is not a substitute for validation; validation must already pass.
- Keep packaging instructions consistent with the plugin template contract.
