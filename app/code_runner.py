import requests
import json


def execute_code(content):
    url = "https://emkc.org/api/v2/piston/execute"
    headers = {
        "Content-Type": "application/json",
        "Cookie": "engineerman.sid=s%3AeUqJ9wNiPM_ZZAjsHC4DwUbttjTyf3pV.IoM11oun22Ux90uHIR9tGsF%2Fwz1tXVDIqq5PDAdFQL0",
    }
    data = {
        "language": "python",
        "version": "3.10.0",
        "files": [{"name": "my_cool_code.py", "content": content}],
        "stdin": "",
        "args": ["1", "2", "3"],
        "compile_timeout": 10000,
        "run_timeout": 3000,
        "compile_memory_limit": -1,
        "run_memory_limit": -1,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    return result["run"]["output"]


# Example usage
code_content = "print('hello, world')"
result = execute_code(code_content)
print(result)
