"""
Health monitoring and maintenance utilities.
"""

import asyncio
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, Any

from ..config import Config
from ..utils.logger import get_logger
from ..services.state import state_manager
from ..services.piston import piston_service

logger = get_logger(__name__)


class HealthMonitor:
    """Health monitoring for the bot."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.last_check = datetime.now()
        self.check_interval = Config.HEALTH_CHECK_INTERVAL
        self.max_memory_mb = Config.MAX_MEMORY_USAGE
        self._running = False
    
    async def start_monitoring(self):
        """Start the health monitoring loop."""
        self._running = True
        logger.info("Health monitoring started")
        
        while self._running:
            try:
                await self._perform_health_check()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in health monitoring: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    def stop_monitoring(self):
        """Stop the health monitoring loop."""
        self._running = False
        logger.info("Health monitoring stopped")
    
    async def _perform_health_check(self):
        """Perform health check."""
        try:
            # Check memory usage
            memory_info = psutil.virtual_memory()
            process = psutil.Process()
            process_memory_mb = process.memory_info().rss / 1024 / 1024
            
            if process_memory_mb > self.max_memory_mb:
                logger.warning(f"High memory usage: {process_memory_mb:.2f}MB")
                await self._cleanup_resources()
            
            # Check uptime
            uptime = datetime.now() - self.start_time
            
            # Cleanup inactive users
            state_manager.cleanup_inactive_users()
            
            # Get stats
            stats = state_manager.get_stats()
            
            logger.info(
                f"Health check - Uptime: {uptime}, "
                f"Memory: {process_memory_mb:.2f}MB, "
                f"Active users: {stats['total_users']}"
            )
            
            self.last_check = datetime.now()
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
    
    async def _cleanup_resources(self):
        """Cleanup resources to free memory."""
        try:
            # Cleanup old user states
            state_manager.cleanup_inactive_users(max_age_hours=1)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            logger.info("Resource cleanup completed")
            
        except Exception as e:
            logger.error(f"Resource cleanup failed: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status."""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                "status": "healthy",
                "uptime": str(datetime.now() - self.start_time),
                "memory_usage_mb": memory_info.rss / 1024 / 1024,
                "last_health_check": self.last_check.isoformat(),
                "user_stats": state_manager.get_stats()
            }
        except Exception as e:
            logger.error(f"Failed to get health status: {e}")
            return {"status": "error", "error": str(e)}


class GracefulShutdown:
    """Handle graceful shutdown of the bot."""
    
    def __init__(self):
        self.shutdown_requested = False
        self.shutdown_timeout = 30
    
    async def shutdown(self, application=None):
        """Perform graceful shutdown."""
        logger.info("Graceful shutdown initiated")
        self.shutdown_requested = True
        
        try:
            # Close HTTP sessions
            if piston_service:
                await piston_service.close()
            
            # Stop the application if provided
            if application:
                await application.stop()
                await application.shutdown()
            
            logger.info("Graceful shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


# Global instances
health_monitor = HealthMonitor()
graceful_shutdown = GracefulShutdown()
