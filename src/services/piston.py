"""
Piston API service for code execution.
"""

import json
import asyncio
from typing import Dict, Optional
import aiohttp
from aiohttp import ClientTimeout, ClientError

from ..config import Config, VERSION_MAPPING
from ..utils.logger import get_logger
from ..utils.helpers import retry_async, sanitize_code_output

logger = get_logger(__name__)


class PistonAPIError(Exception):
    """Custom exception for Piston API errors."""
    pass


class PistonService:
    """Service for interacting with Piston API."""
    
    def __init__(self):
        self.api_url = Config.PISTON_API_URL
        self.timeout = ClientTimeout(total=Config.PISTON_TIMEOUT)
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=Config.CONNECTION_POOL_SIZE,
                ttl_dns_cache=300,
                use_dns_cache=True,
                keepalive_timeout=30,
                enable_cleanup_closed=True
            )
            
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
        
        return self._session
    
    async def close(self):
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    @retry_async(
        max_attempts=Config.PISTON_RETRY_ATTEMPTS,
        delay=Config.PISTON_RETRY_DELAY
    )
    async def execute_code(self, content: str, language: str) -> str:
        """
        Execute code using Piston API.
        
        Args:
            content: Code content to execute
            language: Programming language
        
        Returns:
            Execution output
        
        Raises:
            PistonAPIError: If execution fails
        """
        if not content.strip():
            return "Error: No code provided"
        
        if not language:
            return "Error: No language specified"
        
        data = {
            "language": language,
            "version": VERSION_MAPPING.get(language, "latest"),
            "files": [{"name": f"code.{language}", "content": content}],
            "stdin": "",
            "args": [],
            "compile_timeout": 10000,
            "run_timeout": 3000,
            "compile_memory_limit": -1,
            "run_memory_limit": -1,
        }
        
        session = await self._get_session()
        
        try:
            logger.info(f"Executing {language} code via Piston API")
            
            async with session.post(self.api_url, json=data) as response:
                if response.status == 429:
                    raise PistonAPIError("Rate limited by Piston API")
                
                if response.status >= 500:
                    raise PistonAPIError(f"Piston API server error: {response.status}")
                
                if response.status != 200:
                    error_text = await response.text()
                    raise PistonAPIError(f"HTTP {response.status}: {error_text}")
                
                result = await response.json()
                
                # Handle API response
                if "run" in result:
                    output = result["run"].get("output", "")
                    stderr = result["run"].get("stderr", "")
                    
                    if stderr:
                        output = f"{output}\n{stderr}" if output else stderr
                    
                    if not output:
                        output = "No output"
                    
                elif "compile" in result and result["compile"].get("stderr"):
                    output = f"Compilation error:\n{result['compile']['stderr']}"
                
                else:
                    output = "Error executing code"
                
                return sanitize_code_output(output)
        
        except ClientError as e:
            logger.error(f"Network error executing code: {e}")
            raise PistonAPIError(f"Network error: {e}")
        
        except asyncio.TimeoutError:
            logger.error("Timeout executing code")
            raise PistonAPIError("Code execution timed out")
        
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from Piston API: {e}")
            raise PistonAPIError("Invalid response from code execution service")
        
        except Exception as e:
            logger.error(f"Unexpected error executing code: {e}")
            raise PistonAPIError(f"Unexpected error: {e}")


# Global service instance
piston_service = PistonService()
