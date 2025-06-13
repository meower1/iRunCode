"""
Utilities for error handling and decorators.
"""

import asyncio
import functools
import time
from typing import Any, Callable, Dict, Optional
from collections import defaultdict, deque

from ..utils.logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """Simple rate limiter implementation."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, user_id: str) -> bool:
        """Check if request is allowed for user."""
        now = time.time()
        user_requests = self.requests[user_id]
        
        # Remove old requests outside the window
        while user_requests and user_requests[0] < now - self.window_seconds:
            user_requests.popleft()
        
        # Check if under limit
        if len(user_requests) < self.max_requests:
            user_requests.append(now)
            return True
        
        return False


def retry_async(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator for retrying async functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier for delay
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}"
                    )
                    
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        
        return wrapper
    return decorator


def handle_errors(default_response: Optional[str] = None):
    """
    Decorator for handling errors in handler functions.
    
    Args:
        default_response: Default response to send on error
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                
                # Try to send error message to user if possible
                if default_response and len(args) >= 1:
                    try:
                        update = args[0]
                        if hasattr(update, 'message') and hasattr(update.message, 'reply_text'):
                            await update.message.reply_text(default_response)
                    except Exception as reply_error:
                        logger.error(f"Failed to send error response: {reply_error}")
        
        return wrapper
    return decorator


def sanitize_code_output(output: str, max_length: int = 4000) -> str:
    """
    Sanitize code output for Telegram message.
    
    Args:
        output: Raw output from code execution
        max_length: Maximum length of output
    
    Returns:
        Sanitized output string
    """
    if not output:
        return "No output"
    
    # Remove null bytes and other problematic characters
    output = output.replace('\x00', '').replace('\r\n', '\n').replace('\r', '\n')
    
    # Truncate if too long
    if len(output) > max_length:
        output = output[:max_length] + "\n\n... (output truncated)"
    
    # Escape markdown special characters
    output = output.replace('`', '\\`').replace('*', '\\*').replace('_', '\\_')
    
    return output


def format_exception(e: Exception) -> str:
    """Format exception for user-friendly display."""
    return f"{type(e).__name__}: {str(e)}"
