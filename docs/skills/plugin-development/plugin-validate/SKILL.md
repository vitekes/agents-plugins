---
name: plugin-validate
description: Validate plugin structure, manifest, and implementation using the repository validation script and required plugin checks. Use before considering plugin work complete or ready for packaging or deployment.
---

# Plugin Validate

Use this skill near the end of any plugin change.

## Read First

- [plugin-template/scripts/validate_plugin.py](/C:/Users/vitek/PycharmProjects/agent-plugins/templates/plugin-template/scripts/validate_plugin.py)
- [docs/PLUGIN_DEVELOPMENT_GUIDE.md](/C:/Users/vitek/PycharmProjects/agent/docs/PLUGIN_DEVELOPMENT_GUIDE.md)

## Required Workflow

1. Run plugin validation in strict mode.
2. Run plugin tests relevant to the changed behavior.
3. Confirm manifest, Dockerfile, README, and source structure remain valid.
4. Report validation results explicitly.

## Repository-Specific Rules

- Do not treat plugin work as complete without validation output.
- If validation fails due to a core plugin framework issue, switch to platform-development skills in `agent` and record the reason.
