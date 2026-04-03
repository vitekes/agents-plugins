# Plugin Template

A standardized template for creating deployable plugin packages that follow the platform plugin contract.

This template lives in `agent-plugins` because that repository is the working area for concrete plugin authoring.

The governing contract and platform rules still live in the main `agent` repository.

Terminology note:

- this template is for a plugin package;
- it is not a catalog idea;
- it is not itself a platform runtime module record.

## Quick Start

```bash
# 1. Copy this template
cp -r templates/plugin-template plugins/my-new-plugin

# 2. Update manifest
cd plugins/my-new-plugin
# Edit manifest.json with your plugin details

# 3. Implement your logic
# Edit src/main.py and implement the ExamplePlugin class

# 4. Validate
python scripts/validate_plugin.py . --strict

# 5. Test
pip install -r requirements.txt
pytest tests/

# 6. Build Docker image
docker build -t my-plugin:1.0.0 .

# 7. Submit through the platform control plane
# agent-platform opens and manages the pull request for this repository
```

## Structure

```
my-plugin/
├── manifest.json          # Plugin metadata and configuration
├── src/
│   └── main.py           # Plugin implementation (required)
├── tests/
│   └── test_plugin.py    # Unit tests (recommended)
├── scripts/
│   └── validate_plugin.py # Validation script (optional)
├── Dockerfile            # Container definition (required for deployment)
├── requirements.txt      # Python dependencies (required)
├── README.md             # Documentation (required for production)
└── LICENSE               # License file (recommended)
```

## Requirements

### Mandatory
- ✅ `manifest.json` with valid schema
- ✅ `src/main.py` implementing `BasePlugin`
- ✅ `requirements.txt` with pinned versions
- ✅ `Dockerfile` following security best practices

### Recommended
- 📝 Unit tests with >80% coverage
- 📝 README with usage examples
- 📝 LICENSE file
- 📝 Integration tests

## Plugin Lifecycle

All plugins must implement these methods:

| Method | Purpose | Timeout |
|--------|---------|---------|
| `on_init()` | Initialize resources | 5s |
| `on_activate()` | Enable logic | 1s |
| `on_deactivate()` | Disable logic, drain requests | 30s |
| `on_shutdown()` | Cleanup, save state | 10s |
| `health_check()` | Return health status | 1s |

## Security Rules

Plugins MUST:
- Run as non-root user (UID > 1000)
- Use read-only root filesystem
- Not use `eval()`, `exec()`, or `subprocess`
- Access secrets only via Kubernetes Secrets
- Respect resource quotas

Plugins MUST NOT:
- Access host network directly
- Modify other plugins' data
- Store secrets in environment variables
- Use `:latest` image tags

## Resource Tiers

| Tier | CPU Limit | Memory Limit | Use Case |
|------|-----------|--------------|----------|
| Sandbox | 100m | 128Mi | Testing, experiments |
| Bronze | 500m | 512Mi | Small utilities |
| Silver | 1000m | 1Gi | Standard plugins |
| Gold | 2000m | 2Gi | High-traffic plugins |
| Platinum | 4000m | 4Gi | Critical services |

## Validation

Run validation before submission:

```bash
# Basic validation
python scripts/validate_plugin.py .

# Strict validation (CI/CD requirement)
python scripts/validate_plugin.py . --strict
```

## Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=src

# Type checking
mypy src/

# Linting
ruff check src/
```

## Deployment

Plugin authoring stops at packaging-ready artifacts and deployment inputs. The control-plane repository owns the current deployment orchestration and runtime/module records.

```bash
# Build and publish the plugin image/artifact
docker build -t my-plugin:1.0.0 .

# Hand off deployment metadata to the platform control repository or automation flow
# The platform API tracks runtime modules, releases, and deployments separately.
```

## Examples

See `src/main.py` for a complete example implementation.

## Support

- Documentation: `agent/docs/PLUGIN_DEVELOPMENT_GUIDE.md`
- Contract Spec: `agent/docs/plugin-contract.md`
- Boundary Model: `agent/docs/P5_PLUGIN_CATALOG_ARCHITECTURE.md`
- Issues: GitHub Issues
