# iRunCode Telegram Bot

A professional Telegram bot for executing code snippets in multiple programming languages using the Piston API.

## Features

- **Multi-language Support**: Execute code in 50+ programming languages
- **Interactive Interface**: Button-based language selection and command-line interface
- **Professional Architecture**: Modular, maintainable code structure
- **Error Handling**: Comprehensive error handling and retry mechanisms
- **Rate Limiting**: Built-in rate limiting to prevent abuse
- **Health Monitoring**: Automatic health checks and resource management
- **Docker Support**: Containerized deployment with health checks
- **Graceful Shutdown**: Proper cleanup on termination
- **Logging**: Comprehensive logging with rotation and colored output

## Project Structure

```
iRunCode/
├── src/                          # Source code
│   ├── config/                   # Configuration management
│   │   └── __init__.py          # Config class and constants
│   ├── handlers/                 # Telegram message handlers
│   │   ├── commands.py          # Command handlers (/start, /help, etc.)
│   │   └── messages.py          # Message handlers
│   ├── services/                 # Business logic services
│   │   ├── piston.py            # Piston API integration
│   │   └── state.py             # User state management
│   ├── utils/                    # Utility functions
│   │   ├── logger.py            # Logging configuration
│   │   ├── helpers.py           # Helper functions and decorators
│   │   └── health.py            # Health monitoring
│   └── main.py                  # Application entry point
├── logs/                        # Log files (auto-created)
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yaml          # Docker Compose configuration
├── run.py                      # Startup script
└── README.md                   # This file
```

## Installation

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd iRunCode
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your Telegram Bot API key
   ```

5. **Run the bot**
   ```bash
   python run.py
   # or
   python -m src.main
   ```

### Docker Deployment

1. **Configure environment**

   ```bash
   # Make sure .env file exists with your API_KEY
   echo "API_KEY=your_telegram_bot_token_here" > .env
   ```

2. **Build and run with Docker Compose**

   ```bash
   docker-compose up -d --build
   ```

3. **View logs**

   ```bash
   docker-compose logs -f iruncode-bot
   ```

4. **Stop the bot**
   ```bash
   docker-compose down
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Required
API_KEY=your_telegram_bot_token_here

# Optional - with defaults
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
PISTON_API_URL=https://emkc.org/api/v2/piston/execute
PISTON_TIMEOUT=30
PISTON_RETRY_ATTEMPTS=3
PISTON_RETRY_DELAY=1.0
BOT_TIMEOUT=30
POOLING_TIMEOUT=30
CONNECTION_POOL_SIZE=8
RATE_LIMIT_WINDOW=60
RATE_LIMIT_MAX_REQUESTS=10
HEALTH_CHECK_INTERVAL=300
MAX_MEMORY_USAGE=256
```

## Usage

### Commands

- `/start` - Start the bot and show language selection
- `/help` - Show help message with usage instructions
- `/about` - Show information about the bot
- `/langs` - List all supported programming languages
- `/run <language> <code>` - Execute code directly

### Examples

**Button Interface:**

1. Send `/start`
2. Click on a language button (e.g., "🐍 Python")
3. Send your code
4. Receive the output

**Command Interface:**

```
/run python
print("Hello, World!")
```

**Supported Languages:**
Python, C++, C#, JavaScript, Java, Go, Rust, PHP, C, Bash, and 40+ more languages.

## Key Improvements

### Stability Fixes

1. **Connection Pooling**: Efficient HTTP connection management
2. **Retry Mechanisms**: Automatic retries with exponential backoff
3. **Error Handling**: Comprehensive error catching and user feedback
4. **Rate Limiting**: Prevents API abuse and bot overload
5. **Health Monitoring**: Automatic resource monitoring and cleanup
6. **Graceful Shutdown**: Proper cleanup on termination
7. **Memory Management**: Automatic cleanup of inactive users

### Architecture Improvements

1. **Modular Design**: Separated concerns into logical modules
2. **Configuration Management**: Centralized configuration with validation
3. **Professional Logging**: Structured logging with rotation and colors
4. **Type Hints**: Full type annotations for better code quality
5. **Async/Await**: Proper asynchronous programming throughout
6. **Docker Support**: Production-ready containerization

### Performance Enhancements

1. **Async HTTP Client**: Non-blocking HTTP requests
2. **Connection Reuse**: Persistent HTTP connections
3. **Memory Optimization**: Automatic cleanup of old data
4. **Efficient State Management**: Optimized user state storage

## Monitoring

The bot includes comprehensive monitoring:

- **Health Checks**: Automatic system health monitoring
- **Memory Usage**: Tracks and limits memory consumption
- **User Activity**: Monitors and cleans up inactive users
- **API Performance**: Tracks API response times and errors
- **Logging**: Detailed logs with different levels

## Development

### Adding New Features

1. **Commands**: Add to `src/handlers/commands.py`
2. **Message Handlers**: Add to `src/handlers/messages.py`
3. **Services**: Add business logic to `src/services/`
4. **Configuration**: Update `src/config/__init__.py`

### Testing

```bash
# Run with debug logging
LOG_LEVEL=DEBUG python run.py

# Monitor resource usage
docker stats iruncode
```

## Troubleshooting

### Common Issues

1. **Bot stops responding**: Check logs and restart the container
2. **High memory usage**: Adjust `MAX_MEMORY_USAGE` in environment
3. **API timeouts**: Increase `PISTON_TIMEOUT` setting
4. **Rate limiting**: Adjust rate limit settings in configuration

### Logs

Logs are written to:

- Console (with colors)
- `logs/bot.log` (with rotation)

Use different log levels for different environments:

- `DEBUG`: Development
- `INFO`: Production
- `WARNING`: Production with minimal logs
- `ERROR`: Only errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing code style
4. Add tests if applicable
5. Submit a pull request

## Credits

- [Piston API](https://github.com/engineer-man/piston) by [Engineer Man](https://github.com/engineer-man)
- Built with ❤️ for the community

## License

This project is open source. See the LICENSE file for details.
