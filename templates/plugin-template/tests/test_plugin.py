"""
Plugin Unit Tests

Tests for the plugin template lifecycle.
Run with: pytest tests/test_plugin.py -v
"""

import pytest
import json
from src.main import BasePlugin, PluginError, ExamplePlugin


class TestManifestValidation:
    """Test manifest loading and validation."""

    def test_valid_manifest(self, tmp_path):
        """Test loading a valid manifest."""
        manifest_data = {
            "id": "test-plugin",
            "name": "Test Plugin",
            "version": "1.0.0",
            "entrypoint": "src/main.py"
        }
        
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))
        
        # Should not raise
        plugin = ExamplePlugin(str(manifest_file))
        assert plugin.plugin_id == "test-plugin"
        assert plugin.version == "1.0.0"

    def test_missing_required_field(self, tmp_path):
        """Test that missing required fields raise PluginError."""
        manifest_data = {
            "id": "test-plugin",
            # Missing "name", "version", "entrypoint"
        }
        
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))
        
        with pytest.raises(PluginError) as exc_info:
            ExamplePlugin(str(manifest_file))
        
        assert "Missing required field" in str(exc_info.value)

    def test_invalid_json(self, tmp_path):
        """Test that invalid JSON raises PluginError."""
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text("{ invalid json }")
        
        with pytest.raises(PluginError) as exc_info:
            ExamplePlugin(str(manifest_file))
        
        assert "Invalid JSON" in str(exc_info.value)

    def test_manifest_not_found(self):
        """Test that missing manifest raises PluginError."""
        with pytest.raises(PluginError) as exc_info:
            ExamplePlugin("nonexistent.json")
        
        assert "Manifest not found" in str(exc_info.value)


class TestLifecycle:
    """Test plugin lifecycle methods."""

    @pytest.fixture
    def plugin(self, tmp_path):
        """Create a test plugin instance."""
        manifest_data = {
            "id": "test-plugin",
            "name": "Test Plugin",
            "version": "1.0.0",
            "entrypoint": "src/main.py",
            "lifecycle": {
                "init_timeout": 5,
                "shutdown_timeout": 10,
                "drain_timeout": 30
            }
        }
        
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))
        
        return ExamplePlugin(str(manifest_file))

    def test_init_success(self, plugin):
        """Test successful initialization."""
        result = plugin.init({"key": "value"})
        
        assert result["status"] == "ready"
        assert result["version"] == "1.0.0"
        assert "init_time_ms" in result
        assert plugin._initialized is True

    def test_init_without_config(self, plugin):
        """Test initialization with no config."""
        result = plugin.init()
        
        assert result["status"] == "ready"
        assert plugin._initialized is True

    def test_activate_before_init(self, plugin):
        """Test that activation fails if not initialized."""
        result = plugin.activate()
        
        assert result["status"] == "failed"
        assert "not initialized" in result["error"]

    def test_activate_success(self, plugin):
        """Test successful activation."""
        plugin.init()
        result = plugin.activate()
        
        assert result["status"] == "active"
        assert result["plugin_id"] == "test-plugin"
        assert plugin._active is True

    def test_deactivate_success(self, plugin):
        """Test successful deactivation."""
        plugin.init()
        plugin.activate()
        
        result = plugin.deactivate()
        
        assert result["status"] == "inactive"
        assert plugin._active is False

    def test_deactivate_already_inactive(self, plugin):
        """Test deactivating an already inactive plugin."""
        plugin.init()
        
        result = plugin.deactivate()
        
        assert result["status"] == "already_inactive"

    def test_health_check(self, plugin):
        """Test health check endpoint."""
        result = plugin.health()
        
        assert result["status"] == "healthy"
        assert "checks" in result
        assert result["plugin_id"] == "test-plugin"


class TestExamplePlugin:
    """Test the example plugin implementation."""

    @pytest.fixture
    def example_plugin(self, tmp_path):
        """Create an example plugin instance."""
        manifest_data = {
            "id": "example-plugin",
            "name": "Example Plugin",
            "version": "2.0.0",
            "entrypoint": "src/main.py"
        }
        
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))
        
        return ExamplePlugin(str(manifest_file))

    def test_full_lifecycle(self, example_plugin):
        """Test complete lifecycle: init -> activate -> deactivate -> shutdown."""
        # Init
        init_result = example_plugin.init()
        assert init_result["status"] == "ready"
        
        # Activate
        activate_result = example_plugin.activate()
        assert activate_result["status"] == "active"
        
        # Health check while active
        health_result = example_plugin.health()
        assert health_result["status"] == "healthy"
        
        # Deactivate
        deactivate_result = example_plugin.deactivate()
        assert deactivate_result["status"] == "inactive"
        
        # Shutdown (should not raise)
        example_plugin.shutdown()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
