import requests
import json


def execute_code(content, language):
    # Language version mapping (you can adjust versions as needed)
    version_mapping = {
        "python": "3.10.0",
        "cpp": "10.2.0",
        "csharp": "10.0",
        "bash": "5.1.0",
        "go": "1.16.2",
        "c": "10.2.0",
        "brainfuck": "2.7.3",
        "javascript": "1.32.3",
        "php": "8.2.3",
        "rust": "1.68.2",
        "java": "15.0.2",
    }

    url = "https://emkc.org/api/v2/piston/execute"
    headers = {
        "Content-Type": "application/json",
    }

    # Set up data with the appropriate language and version
    data = {
        "language": language,
        "version": version_mapping.get(
            language, "latest"
        ),  # Default to 'latest' if no version is found
        "files": [{"name": f"code.{language}", "content": content}],
        "stdin": "",
        "args": [],
        "compile_timeout": 10000,
        "run_timeout": 3000,
        "compile_memory_limit": -1,
        "run_memory_limit": -1,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()

    # Return the output or error
    return result.get("run", {}).get("output", "Error executing code.")
