"""
Plugin Entry Point

This module implements the standard plugin lifecycle interface.
All plugins MUST inherit from BasePlugin and implement required methods.
"""

import os
import sys
import json
import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import signal
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PluginError(Exception):
    """Base exception for plugin errors."""
    pass


class BasePlugin(ABC):
    """
    Abstract base class for all plugins.
    Implements the standard lifecycle interface.
    """

    def __init__(self, manifest_path: str = "manifest.json"):
        self.manifest = self._load_manifest(manifest_path)
        self.plugin_id = self.manifest.get("id")
        self.version = self.manifest.get("version")
        self._active = False
        self._initialized = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._handle_shutdown_signal)
        signal.signal(signal.SIGINT, self._handle_shutdown_signal)

    def _load_manifest(self, path: str) -> Dict[str, Any]:
        """Load and validate plugin manifest."""
        try:
            with open(path, 'r') as f:
                manifest = json.load(f)
            
            # Validate required fields
            required_fields = ["id", "name", "version", "entrypoint"]
            for field in required_fields:
                if field not in manifest:
                    raise PluginError(f"Missing required field in manifest: {field}")
            
            return manifest
        except FileNotFoundError:
            raise PluginError(f"Manifest not found at {path}")
        except json.JSONDecodeError as e:
            raise PluginError(f"Invalid JSON in manifest: {e}")

    @abstractmethod
    def on_init(self, config: Dict[str, Any]) -> bool:
        """
        Initialize plugin resources.
        Called once upon startup.
        Must complete within init_timeout (default 5s).
        
        Returns:
            bool: True if initialization successful, False otherwise.
        """
        pass

    @abstractmethod
    def on_activate(self) -> bool:
        """
        Activate plugin logic.
        Called when feature flag is enabled.
        
        Returns:
            bool: True if activation successful, False otherwise.
        """
        pass

    @abstractmethod
    def on_deactivate(self) -> bool:
        """
        Deactivate plugin logic.
        Called when feature flag is disabled.
        Should drain existing requests within drain_timeout.
        
        Returns:
            bool: True if deactivation successful, False otherwise.
        """
        pass

    @abstractmethod
    def on_shutdown(self) -> None:
        """
        Graceful shutdown.
        Save state, close connections, cleanup resources.
        Must complete within shutdown_timeout (default 10s).
        """
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check.
        Must return within 1s.
        
        Returns:
            dict: {"status": "healthy|degraded", "checks": {...}}
        """
        pass

    # === Lifecycle Methods (Do Not Override) ===

    def init(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Standard init endpoint implementation."""
        start_time = time.time()
        timeout = self.manifest.get("lifecycle", {}).get("init_timeout", 5)
        
        try:
            config = config or {}
            success = self.on_init(config)
            
            if not success:
                raise PluginError("Initialization returned False")
            
            self._initialized = True
            elapsed = time.time() - start_time
            
            logger.info(f"Plugin {self.plugin_id} initialized in {elapsed:.2f}s")
            
            return {
                "status": "ready",
                "version": self.version,
                "init_time_ms": int(elapsed * 1000)
            }
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "version": self.version
            }

    def activate(self) -> Dict[str, Any]:
        """Standard activate endpoint implementation."""
        try:
            if not self._initialized:
                raise PluginError("Plugin not initialized. Call init() first.")
            
            success = self.on_activate()
            
            if not success:
                raise PluginError("Activation returned False")
            
            self._active = True
            logger.info(f"Plugin {self.plugin_id} activated")
            
            return {"status": "active", "plugin_id": self.plugin_id}
            
        except Exception as e:
            logger.error(f"Activation failed: {e}")
            return {"status": "failed", "error": str(e)}

    def deactivate(self) -> Dict[str, Any]:
        """Standard deactivate endpoint implementation."""
        try:
            if not self._active:
                return {"status": "already_inactive", "plugin_id": self.plugin_id}
            
            success = self.on_deactivate()
            
            if not success:
                raise PluginError("Deactivation returned False")
            
            self._active = False
            logger.info(f"Plugin {self.plugin_id} deactivated")
            
            return {"status": "inactive", "plugin_id": self.plugin_id}
            
        except Exception as e:
            logger.error(f"Deactivation failed: {e}")
            return {"status": "failed", "error": str(e)}

    def health(self) -> Dict[str, Any]:
        """Standard health endpoint implementation."""
        try:
            result = self.health_check()
            
            if not isinstance(result, dict) or "status" not in result:
                raise PluginError("health_check must return dict with 'status' key")
            
            return result
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "plugin_id": self.plugin_id
            }

    def _handle_shutdown_signal(self, signum, frame):
        """Handle SIGTERM/SIGINT for graceful shutdown."""
        logger.info(f"Received signal {signum}, initiating shutdown...")
        self.shutdown()
        sys.exit(0)

    def shutdown(self) -> None:
        """Standard shutdown endpoint implementation."""
        try:
            logger.info(f"Plugin {self.plugin_id} shutting down...")
            self.on_shutdown()
            logger.info(f"Plugin {self.plugin_id} shutdown complete")
        except Exception as e:
            logger.error(f"Shutdown error: {e}")
            # Force exit on error after timeout
            os._exit(1)


# === Example Implementation ===

class ExamplePlugin(BasePlugin):
    """
    Example plugin implementation.
    Copy this class and implement the abstract methods.
    """

    def on_init(self, config: Dict[str, Any]) -> bool:
        logger.info(f"Initializing {self.plugin_id} with config: {config}")
        # TODO: Add your initialization logic here
        # - Connect to databases
        # - Load models
        # - Validate configuration
        return True

    def on_activate(self) -> bool:
        logger.info(f"Activating {self.plugin_id}")
        # TODO: Add your activation logic here
        # - Start background workers
        # - Enable request handlers
        return True

    def on_deactivate(self) -> bool:
        logger.info(f"Deactivating {self.plugin_id}")
        # TODO: Add your deactivation logic here
        # - Stop background workers
        # - Drain pending requests
        time.sleep(1)  # Simulate draining
        return True

    def on_shutdown(self) -> None:
        logger.info(f"Shutting down {self.plugin_id}")
        # TODO: Add your shutdown logic here
        # - Save state
        # - Close connections
        pass

    def health_check(self) -> Dict[str, Any]:
        # TODO: Add your health check logic here
        # - Check database connectivity
        # - Check memory usage
        # - Check dependent services
        return {
            "status": "healthy",
            "checks": {
                "memory": "ok",
                "connections": "ok"
            },
            "plugin_id": self.plugin_id
        }


# === HTTP Server Wrapper (for standalone plugins) ===

if __name__ == "__main__":
    # This allows the plugin to run as a standalone HTTP service
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json
    
    plugin = ExamplePlugin()
    
    class PluginHandler(BaseHTTPRequestHandler):
        def _send_response(self, data: Dict[str, Any], status: int = 200):
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode() if content_length > 0 else '{}'
            
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self._send_response({"error": "Invalid JSON"}, 400)
                return
            
            if self.path == '/init':
                result = plugin.init(data.get('config'))
            elif self.path == '/activate':
                result = plugin.activate()
            elif self.path == '/deactivate':
                result = plugin.deactivate()
            elif self.path == '/shutdown':
                plugin.shutdown()
                self._send_response({"status": "shutting_down"})
                return
            else:
                self._send_response({"error": "Not found"}, 404)
                return
            
            self._send_response(result)
        
        def do_GET(self):
            if self.path == '/health':
                result = plugin.health()
            else:
                self._send_response({"error": "Not found"}, 404)
                return
            
            self._send_response(result)
        
        def log_message(self, format, *args):
            logger.info(f"{self.address_string()} - {format % args}")
    
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), PluginHandler)
    logger.info(f"Plugin {plugin.plugin_id} starting on port {port}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        plugin.shutdown()
