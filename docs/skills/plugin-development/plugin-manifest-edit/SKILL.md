---
name: plugin-manifest-edit
description: Edit plugin manifest metadata, resources, permissions, lifecycle settings, and packaging metadata for plugins created from this repository template. Use when changing manifest.json or plugin identity and deployment metadata.
---

# Plugin Manifest Edit

Use this skill for `manifest.json` changes in plugin work.

## Read First

- [plugin-template/manifest.json](/C:/Users/vitek/PycharmProjects/agent-plugins/templates/plugin-template/manifest.json)
- [plugin-template/manifest.schema.json](/C:/Users/vitek/PycharmProjects/agent-plugins/templates/plugin-template/manifest.schema.json)
- [docs/plugin-contract.md](/C:/Users/vitek/PycharmProjects/agent/docs/plugin-contract.md)

## Required Workflow

1. Update plugin identity, description, resources, permissions, and entrypoint consistently.
2. Keep the manifest compatible with the schema.
3. Re-run validation after edits.

## Repository-Specific Rules

- Do not add permissions or resource tiers casually.
- Keep lifecycle and packaging metadata consistent with the actual implementation.
