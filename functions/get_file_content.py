import os
from google.genai import types
from functions.utils import issubdir


def get_file_content(working_directory: str, file_path: str) -> str:
    full_path = os.path.join(working_directory, file_path)

    if not issubdir(full_path, working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000
        with open(full_path, "r") as f:
            content = f.read(MAX_CHARS)
            size = os.path.getsize(full_path)

            if size > MAX_CHARS:
                content += f'[...File "{file_path}" truncated at 10000 characters]'

            return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets maximum of 10000 characters from file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get characters from, relative to the working directory.",
            ),
        },
    ),
)
