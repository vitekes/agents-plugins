---
name: plugin-test
description: Add and run plugin-focused tests for lifecycle behavior, validation cases, and local plugin logic. Use when plugin behavior changes or when preparing plugin work for validation and packaging.
---

# Plugin Test

Use this skill for plugin test work.

## Read First

- [plugin-template/tests/test_plugin.py](/C:/Users/vitek/PycharmProjects/agent-plugins/templates/plugin-template/tests/test_plugin.py)
- [docs/PLUGIN_DEVELOPMENT_GUIDE.md](/C:/Users/vitek/PycharmProjects/agent/docs/PLUGIN_DEVELOPMENT_GUIDE.md)

## Required Workflow

1. Add or update tests for the changed plugin behavior.
2. Cover lifecycle and validation-relevant cases, not only happy paths.
3. Run the smallest sufficient plugin test set.

## Repository-Specific Rules

- Plugin lifecycle changes must be backed by tests when behavior changes materially.
- Do not rely only on manifest validation for runtime behavior confidence.
