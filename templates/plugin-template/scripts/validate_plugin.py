#!/usr/bin/env python3
"""
Plugin Validator Script

Validates plugin structure, manifest schema, and security requirements.
Used in CI pipelines to ensure plugins meet standards before deployment.

Usage:
    python validate_plugin.py /path/to/plugin
    python validate_plugin.py --strict /path/to/plugin
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class PluginValidator:
    """Validates plugin structure and manifest."""

    REQUIRED_FILES = ["manifest.json", "src/main.py", "requirements.txt"]
    FORBIDDEN_PATTERNS = [
        "__import__('os').system",
        "subprocess.call",
        "subprocess.run",
        "eval(",
        "exec(",
        "pickle.load",
        "yaml.load(unsafe",
    ]

    def __init__(self, plugin_path: str, strict: bool = False):
        self.plugin_path = Path(plugin_path)
        self.strict = strict
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.manifest: Dict[str, Any] = {}

    def validate(self) -> bool:
        """Run all validations. Returns True if valid."""
        print(f"Validating plugin at: {self.plugin_path}")
        print("-" * 50)

        try:
            self._check_directory_exists()
            self._check_required_files()
            self._load_and_validate_manifest()
            self._check_security()
            self._check_structure()

            if self.strict:
                self._check_strict_requirements()

        except ValidationError as e:
            self.errors.append(str(e))

        self._print_report()
        return len(self.errors) == 0

    def _check_directory_exists(self):
        """Check if plugin directory exists."""
        if not self.plugin_path.exists():
            raise ValidationError(f"Plugin directory does not exist: {self.plugin_path}")
        if not self.plugin_path.is_dir():
            raise ValidationError(f"Path is not a directory: {self.plugin_path}")

    def _check_required_files(self):
        """Check for required files."""
        for file in self.REQUIRED_FILES:
            file_path = self.plugin_path / file
            if not file_path.exists():
                self.errors.append(f"Missing required file: {file}")
            elif file_path.stat().st_size == 0:
                self.warnings.append(f"File is empty: {file}")

    def _load_and_validate_manifest(self):
        """Load and validate manifest.json."""
        manifest_path = self.plugin_path / "manifest.json"
        if not manifest_path.exists():
            return

        try:
            with open(manifest_path, "r") as f:
                self.manifest = json.load(f)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in manifest: {e}")

        self._validate_manifest_schema()

        required_fields = ["id", "name", "version", "entrypoint"]
        for field in required_fields:
            if field not in self.manifest:
                self.errors.append(f"Missing required field in manifest: {field}")

        if "id" in self.manifest:
            plugin_id = self.manifest["id"]
            if not plugin_id.replace("-", "").isalnum():
                self.errors.append(f"Invalid plugin ID format: {plugin_id}")
            if len(plugin_id) < 3 or len(plugin_id) > 64:
                self.errors.append(f"Plugin ID must be 3-64 chars: {plugin_id}")

        if "version" in self.manifest:
            version = self.manifest["version"]
            parts = version.split(".")
            if len(parts) != 3:
                self.errors.append(f"Version must be MAJOR.MINOR.PATCH: {version}")
            else:
                try:
                    int(parts[0]), int(parts[1].split("-")[0]), int(parts[2].split("-")[0])
                except ValueError:
                    self.errors.append(f"Version components must be integers: {version}")

        if "resources" in self.manifest:
            resources = self.manifest["resources"]
            valid_tiers = ["sandbox", "bronze", "silver", "gold", "platinum"]
            if "tier" in resources and resources["tier"] not in valid_tiers:
                self.errors.append(f"Invalid resource tier: {resources['tier']}")

        self._validate_ai_configuration()

        if "description" in self.manifest and len(self.manifest["description"]) > 140:
            self.warnings.append("Short description should be under 140 characters for catalog display")

        if "long_description" not in self.manifest:
            self.warnings.append("Missing 'long_description' - recommended for catalog visibility")

    def _validate_manifest_schema(self):
        """Validate manifest against JSON schema."""
        try:
            import jsonschema

            template_root = Path(__file__).resolve().parent.parent
            schema_locations = [
                template_root / "manifest.schema.json",
                self.plugin_path / "manifest.schema.json",
                Path(__file__).parent / "manifest.schema.json",
            ]

            schema_file = None
            for loc in schema_locations:
                if loc.exists():
                    schema_file = loc
                    break

            if schema_file and schema_file.exists():
                with open(schema_file, "r") as f:
                    schema = json.load(f)
                jsonschema.validate(self.manifest, schema)
            else:
                self.warnings.append("manifest.schema.json not found - skipping schema validation")
        except ImportError:
            self.warnings.append("jsonschema not installed - skipping schema validation")
        except jsonschema.ValidationError as e:
            self.errors.append(f"Manifest schema validation failed: {e.message}")
        except Exception as e:
            self.warnings.append(f"Could not validate schema: {e}")

    def _validate_ai_configuration(self):
        """Validate AI configuration if present."""
        if "ai_configuration" not in self.manifest:
            return

        ai_config = self.manifest["ai_configuration"]

        if ai_config.get("enabled", False) and "environments" not in ai_config:
            self.errors.append("AI enabled but no environments configured")
            return

        if "environments" not in ai_config:
            return

        envs = ai_config["environments"]

        if ai_config.get("enabled", False) and "production" not in envs:
            self.errors.append("Production environment must be defined when AI is enabled")

        if "production" in envs:
            prod = envs["production"]
            if "max_tokens" not in prod:
                self.errors.append("Production environment missing max_tokens limit")
            elif prod["max_tokens"] > 4096:
                self.warnings.append(
                    f"Production max_tokens ({prod['max_tokens']}) seems high. Consider reducing for cost optimization."
                )

            if "budget_daily_usd" not in prod:
                self.warnings.append("Production environment missing budget_daily_usd - recommended for cost control")

        if "development" in envs and "production" in envs:
            dev_models = set(envs["development"].get("models", []))
            prod_models = set(envs["production"].get("models", []))

            expensive_models = {"gpt-4o", "gpt-4-turbo", "claude-3-opus", "claude-3-sonnet"}
            if dev_models & expensive_models and prod_models & expensive_models:
                self.warnings.append(
                    "Consider using cheaper models in production (e.g., gpt-4o-mini, claude-3-haiku) "
                    "to reduce costs. Development can use higher-quality models."
                )

    def _check_security(self):
        """Security checks on source files."""
        src_path = self.plugin_path / "src"
        if not src_path.exists():
            return

        for py_file in src_path.glob("**/*.py"):
            try:
                content = py_file.read_text()

                for pattern in self.FORBIDDEN_PATTERNS:
                    if pattern in content:
                        if self.strict:
                            self.errors.append(f"Forbidden pattern in {py_file.name}: {pattern}")
                        else:
                            self.warnings.append(f"Potentially unsafe pattern in {py_file.name}: {pattern}")

            except Exception as e:
                self.warnings.append(f"Could not read {py_file}: {e}")

    def _check_structure(self):
        """Check directory structure."""
        src_path = self.plugin_path / "src"
        if src_path.exists() and not src_path.is_dir():
            self.errors.append("'src' must be a directory")

        tests_path = self.plugin_path / "tests"
        if not tests_path.exists():
            self.warnings.append("No tests directory found. Consider adding tests.")

    def _check_strict_requirements(self):
        """Additional checks for strict mode."""
        if not (self.plugin_path / "Dockerfile").exists():
            self.errors.append("Missing Dockerfile (required in strict mode)")

        readme_found = any([
            (self.plugin_path / "README.md").exists(),
            (self.plugin_path / "README.rst").exists(),
        ])
        if not readme_found:
            self.errors.append("Missing README (required in strict mode)")

        if "author" not in self.manifest:
            self.errors.append("Missing 'author' field in manifest (required in strict mode)")

        license_found = any([
            (self.plugin_path / "LICENSE").exists(),
            (self.plugin_path / "LICENSE.md").exists(),
            (self.plugin_path / "LICENSE.txt").exists(),
        ])
        if not license_found:
            self.warnings.append("No LICENSE file found. Consider adding one.")

    def _print_report(self):
        """Print validation report."""
        print()

        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
            print()

        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()

        if not self.errors and not self.warnings:
            print("Validation passed with no issues.")
        elif not self.errors:
            print("Validation passed with warnings.")
        else:
            print("Validation FAILED.")

        print("-" * 50)
        print(f"Errors: {len(self.errors)}, Warnings: {len(self.warnings)}")


def main():
    parser = argparse.ArgumentParser(description="Validate plugin structure and manifest")
    parser.add_argument("plugin_path", help="Path to plugin directory")
    parser.add_argument("--strict", action="store_true", help="Enable strict validation mode")

    args = parser.parse_args()

    validator = PluginValidator(args.plugin_path, strict=args.strict)
    is_valid = validator.validate()

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
