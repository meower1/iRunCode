#!/usr/bin/env python3
"""
Startup script for the iRunCode Telegram bot.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
