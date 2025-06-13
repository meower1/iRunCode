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
    "select_language_first": "🚀 **iRunCode Bot - How to Use**\n\n"
                           "**Method 1: Use Language Buttons**\n"
                           "• Click a language button (🐍 Python, 💻 C++, etc.)\n"
                           "• Send your code\n"
                           "• Get results!\n\n"
                           "**Method 2: Use /run Command**\n"
                           "• Type: `/run <language>`\n"
                           "• Send your code on next line\n"
                           "• Example: `/run python` then `print('Hello!')`\n\n"
                           "**Method 3: See All Languages**\n"
                           "• Use `/langs` for popular languages\n"
                           "• Click '👾 Other Languages' for complete list\n\n"
                           "💡 **Tip**: Need help? Use `/help` command!",
    "invalid_language": "❌ **Invalid Language Selection**\n\n"
                       "Please select a valid programming language from:\n"
                       "• The language buttons shown\n"
                       "• Use `/langs` to see popular languages\n"
                       "• Click '👾 Other Languages' for complete list\n"
                       "• Use `/help` for detailed instructions",
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

# Comprehensive language categories for better organization
LANGUAGE_CATEGORIES = {
    "🔥 Popular Languages": [
        ("python", "Python 3.10.0", "🐍"),
        ("javascript", "JavaScript 1.32.3", "🟨"),
        ("java", "Java 15.0.2", "☕"),
        ("cpp", "C++ 10.2.0", "💻"),
        ("csharp", "C# 10.0", "📚"),
        ("go", "Go 1.16.2", "🦄"),
        ("rust", "Rust 1.68.2", "🦀"),
        ("php", "PHP 8.2.3", "🧑‍💻"),
        ("ruby", "Ruby", "💎"),
        ("typescript", "TypeScript 5.0.3", "📘"),
    ],
    "🖥️ Systems & Low-Level": [
        ("c", "C 10.2.0", "🖥️"),
        ("cpp", "C++ 10.2.0", "💻"),
        ("rust", "Rust 1.68.2", "🦀"),
        ("go", "Go 1.16.2", "🦄"),
        ("zig", "Zig", "⚡"),
        ("nasm", "NASM", "🔧"),
        ("nasm64", "NASM64", "🔧"),
    ],
    "🌐 Web Technologies": [
        ("javascript", "JavaScript 1.32.3", "🟨"),
        ("typescript", "TypeScript 5.0.3", "📘"),
        ("php", "PHP 8.2.3", "🧑‍💻"),
        ("coffeescript", "CoffeeScript 2.5.1", "☕"),
    ],
    "📱 Mobile & Modern": [
        ("swift", "Swift", "🍎"),
        ("kotlin", "Kotlin", "📳"),
        ("dart", "Dart 2.19.6", "🎯"),
        ("crystal", "Crystal 0.36.1", "💎"),
    ],
    "🧠 Functional Programming": [
        ("haskell", "Haskell", "🧠"),
        ("clojure", "Clojure 1.10.3", "🌿"),
        ("erlang", "Erlang", "📡"),
        ("elixir", "Elixir", "💜"),
        ("racket", "Racket", "🎾"),
        ("lisp", "Lisp", "🧙‍♂️"),
        ("fsharp.net", "F# .NET", "🔷"),
    ],
    "🔬 Data Science & Math": [
        ("python", "Python 3.10.0", "🐍"),
        ("julia", "Julia", "🔬"),
        ("rscript", "R", "📊"),
        ("octave", "Octave", "🧮"),
        ("matl", "MATL 22.7.4", "🔢"),
    ],
    "🎮 Esoteric & Fun": [
        ("brainfuck", "Brainfuck", "🧠"),
        ("befunge93", "Befunge93 0.2.0", "🎯"),
        ("lolcode", "LOLCODE", "😂"),
        ("cow", "COW 1.0.0", "🐄"),
        ("rockstar", "Rockstar", "🎸"),
        ("emojicode", "Emojicode", "😀"),
    ],
    "🏢 Enterprise & Legacy": [
        ("java", "Java 15.0.2", "☕"),
        ("csharp", "C# 10.0", "📚"),
        ("cobol", "COBOL 3.1.2", "🏢"),
        ("pascal", "Pascal", "📐"),
        ("fortran", "Fortran", "⚙️"),
        ("scala", "Scala", "🎭"),
    ],
    "🐚 Scripting & Automation": [
        ("bash", "Bash 5.2.0", "🐚"),
        ("powershell", "PowerShell", "💙"),
        ("perl", "Perl", "🐪"),
        ("awk", "AWK", "🔧"),
        ("lua", "Lua", "🌙"),
    ],
    "🔮 Specialized Languages": [
        ("sql", "SQL", "🗄️"),
        ("sqlite3", "SQLite3", "💾"),
        ("prolog", "Prolog", "🧠"),
        ("nim", "Nim", "👑"),
        ("vlang", "V", "🅥"),
        ("groovy", "Groovy", "🎵"),
        ("smalltalk", "Smalltalk", "💬"),
    ]
}

# Usage examples for different language categories
USAGE_EXAMPLES = {
    "python": {
        "example": "print('Hello, World!')\nfor i in range(5):\n    print(f'Number: {i}')",
        "description": "High-level programming language, great for beginners"
    },
    "javascript": {
        "example": "console.log('Hello, World!');\nconst arr = [1, 2, 3];\nconsole.log(arr.map(x => x * 2));",
        "description": "The language of the web, used for frontend and backend"
    },
    "java": {
        "example": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
        "description": "Object-oriented language, popular for enterprise applications"
    },
    "cpp": {
        "example": "#include <iostream>\nint main() {\n    std::cout << \"Hello, World!\" << std::endl;\n    return 0;\n}",
        "description": "Low-level language with high performance"
    },
    "brainfuck": {
        "example": "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
        "description": "Esoteric programming language - just for fun!"
    }
}
