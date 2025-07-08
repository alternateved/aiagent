import os
import subprocess
from functions.utils import issubdir


def run_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    if not issubdir(full_path, working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    if os.path.splitext(full_path)[-1] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        process = subprocess.run(
            ["python", full_path], capture_output=True, text=True, timeout=30
        )

        result = []
        if len(process.stdout) == 0 and len(process.stderr) == 0:
            result.append("No output produced.")
        else:
            result.append(f"STDOUT: {process.stdout}")
            result.append(f"STDERR: {process.stderr}")

        if process.returncode != 0:
            result.append(f"Process exited with code {process.returncode}")

        return "\n".join(result)

    except Exception as e:
        return f"Error: executing Python file: {e}"
