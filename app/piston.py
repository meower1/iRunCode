import requests
import json


def execute_code(content, language):
    version_mapping = {
        "python": "3.10.0",
        "cpp": "10.2.0",
        "csharp": "10.0",
        "bash": "5.2.0",  # Updated version
        "go": "1.16.2",
        "c": "10.2.0",
        "brainfuck": "2.7.3",
        "javascript": "1.32.3",
        "php": "8.2.3",
        "rust": "1.68.2",
        "java": "15.0.2",
        # Newly added languages
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
        # Add more from the provided list as necessary
    }

    url = "https://emkc.org/api/v2/piston/execute"
    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "language": language,
        "version": version_mapping.get(language, "latest"),
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

    return result.get("run", {}).get("output", "Error executing code.")
