import requests
import json


def execute_code(content, language):
    url = "https://emkc.org/api/v2/piston/execute"
    headers = {
        "Content-Type": "application/json",
        # Add your own cookie or authentication header if needed
    }

    # You might need to handle specific versions per language here, modify if needed
    language_versions = {
        "python": "3.10.0",
        "cpp": "10.2.0",  # Example version for C++
        "csharp": "6.12.0",  # Example version for C#
        "bash": "5.2.0",  # Example version for Bash
    }

    # Get the correct version for the selected language, default to a safe version
    version = language_versions.get(language, "3.10.0")

    # Prepare the data payload
    data = {
        "language": language,
        "version": version,
        "files": [{"name": f"my_cool_code.{language}", "content": content}],
        "stdin": "",
        "args": ["1", "2", "3"],
        "compile_timeout": 10000,
        "run_timeout": 3000,
        "compile_memory_limit": -1,
        "run_memory_limit": -1,
    }

    # Make the request to the Piston API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Handle potential errors from the API
    if response.status_code == 200:
        result = response.json()
        return result["run"]["output"]
    else:
        return f"Error: {response.status_code}, {response.text}"
