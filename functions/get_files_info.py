import os
from functions.utils import issubdir


def get_files_info(working_directory: str, directory: str | None = None) -> str:
    full_path = os.path.join(working_directory, directory or ".")

    if not issubdir(full_path, working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        result = []
        for file in os.listdir(full_path):
            path = os.path.join(full_path, file)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            result.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(result)

    except Exception as e:
        return f"Error: {e}"
