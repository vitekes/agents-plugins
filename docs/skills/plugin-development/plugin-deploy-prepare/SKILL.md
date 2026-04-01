---
name: plugin-deploy-prepare
description: Prepare a validated plugin for preview, staging, or approved deployment by aligning deployment inputs, resource assumptions, and documentation. Use when plugin work moves toward deployment planning but before actual rollout execution.
---

# Plugin Deploy Prepare

Use this skill for pre-deployment plugin work.

## Read First

- [docs/PLUGIN_DEVELOPMENT_GUIDE.md](/C:/Users/vitek/PycharmProjects/agent/docs/PLUGIN_DEVELOPMENT_GUIDE.md)
- [docs/DEPLOYMENT.md](/C:/Users/vitek/PycharmProjects/agent/docs/DEPLOYMENT.md)
- [docs/P5_PLUGIN_CATALOG_ARCHITECTURE.md](/C:/Users/vitek/PycharmProjects/agent/docs/P5_PLUGIN_CATALOG_ARCHITECTURE.md)

## Required Workflow

1. Verify the plugin has passed validation and testing.
2. Confirm resource and lifecycle assumptions match the intended deployment target.
3. Prepare deployment-facing metadata, packaging outputs, or handoff instructions for the platform control plane.
4. Update docs if operational steps changed.

## Repository-Specific Rules

- Do not treat deploy preparation as approval to deploy.
- Keep preview, staging, and production expectations separate.
- Do not treat plugin packaging as the same thing as creating runtime module, release, or deployment records in the platform API.
