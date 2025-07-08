import os
from google.genai import types
from functions.utils import issubdir


def write_file(working_directory: str, file_path: str, content: str) -> str:
    full_path = os.path.join(working_directory, file_path)

    if not issubdir(full_path, working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        dir = os.path.dirname(full_path)
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to file, constrained to the working directory. Return number of characters written.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write content to. If that file doesn't exist, it will be created. Relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content of the file.",
            ),
        },
    ),
)
