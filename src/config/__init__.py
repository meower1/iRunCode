"""
Configuration module for the Telegram bot.
Contains all configuration settings, constants, and environment variables.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the bot."""
    
    # Telegram Bot Configuration
    API_KEY: str = os.getenv("API_KEY", "")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/bot.log")
    
    # Piston API Configuration
    PISTON_API_URL: str = os.getenv("PISTON_API_URL", "https://emkc.org/api/v2/piston/execute")
    PISTON_TIMEOUT: int = int(os.getenv("PISTON_TIMEOUT", "30"))
    PISTON_RETRY_ATTEMPTS: int = int(os.getenv("PISTON_RETRY_ATTEMPTS", "3"))
    PISTON_RETRY_DELAY: float = float(os.getenv("PISTON_RETRY_DELAY", "1.0"))
    
    # Bot Configuration
    BOT_TIMEOUT: int = int(os.getenv("BOT_TIMEOUT", "30"))
    POOLING_TIMEOUT: int = int(os.getenv("POOLING_TIMEOUT", "30"))
    CONNECTION_POOL_SIZE: int = int(os.getenv("CONNECTION_POOL_SIZE", "8"))
    
    # Rate Limiting
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "10"))
    
    # Health Check Configuration
    HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "300"))  # 5 minutes
    MAX_MEMORY_USAGE: int = int(os.getenv("MAX_MEMORY_USAGE", "256"))  # MB
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration."""
        if not cls.API_KEY:
            raise ValueError("API_KEY environment variable is required")
        
        if not cls.API_KEY.strip():
            raise ValueError("API_KEY cannot be empty")


# Language configurations
LANGUAGES: Dict[str, str] = {
    "🐍 Python": "python",
    "💻 C++": "cpp",
    "📚 C#": "csharp",
    "🐚 Bash": "bash",
    "🦄 Go": "go",
    "🖥 C": "c",
    "🧠 Brainfuck": "brainfuck",
    "🖥 JavaScript": "javascript",
    "🧑‍💻 PHP": "php",
    "🦀 Rust": "rust",
    "☕️ Java": "java",
}

# Version mapping for Piston API
VERSION_MAPPING: Dict[str, str] = {
    "python": "3.10.0",
    "cpp": "10.2.0",
    "csharp": "10.0",
    "bash": "5.2.0",
    "go": "1.16.2",
    "c": "10.2.0",
    "brainfuck": "2.7.3",
    "javascript": "1.32.3",
    "php": "8.2.3",
    "rust": "1.68.2",
    "java": "15.0.2",
    "matl": "22.7.4",
    "befunge93": "0.2.0",
    "bqn": "1.0.0",
    "brachylog": "1.0.0",
    "cjam": "0.6.5",
    "clojure": "1.10.3",
    "cobol": "3.1.2",
    "coffeescript": "2.5.1",
    "cow": "1.0.0",
    "crystal": "0.36.1",
    "dart": "2.19.6",
    "typescript": "5.0.3",
}

# Bot messages
MESSAGES: Dict[str, str] = {
    "welcome": "Welcome {name}. Select a language to run your code:",
    "language_selected": "You selected {language}. Please enter your code. Press 'Return' when you're done.",
    "exit_code_mode": "Exited code input mode. Select another language:",
    "select_language_first": "Please select a language first using the /run command or the buttons.",
    "invalid_language": "Please select a valid programming language.",
    "output_prefix": "Output:\n```\n{output}\n```",
    "error_executing": "Error executing code: {error}",
    "rate_limited": "Rate limited. Please wait before sending another request.",
    "service_unavailable": "Service temporarily unavailable. Please try again later.",
}

# Supported languages text
SUPPORTED_LANGUAGES_TEXT = (
    "awk, bash, basic, basic.net, befunge93, bqn, brachylog, brainfuck, c, c++, "
    "cjam, clojure, cobol, coffeescript, cow, crystal, csharp, csharp.net, d, dart, "
    "dash, dragon, elixir, emacs, emojicode, erlang, file, forte, forth, fortran, "
    "freebasic, fsharp.net, fsi, go, golfscript, groovy, haskell, husk, iverilog, "
    "japt, java, javascript, jelly, julia, kotlin, lisp, llvm_ir, lolcode, lua, "
    "matl, nasm, nasm64, nim, ocaml, octave, osabie, paradoc, pascal, perl, php, "
    "ponylang, powershell, prolog, pure, pyth, python, python2, racket, raku, "
    "retina, rockstar, rscript, ruby, rust, samarium, scala, smalltalk, sqlite3, "
    "swift, typescript, vlang, vyxal, yeethon, zig"
)
