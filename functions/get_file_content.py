import os


def get_file_content(working_directory: str, file_path: str) -> str:
    full_path = os.path.join(working_directory, file_path)
    working_directory_abspath = os.path.abspath(working_directory)
    full_path_abspath = os.path.abspath(full_path)

    if not full_path_abspath.startswith(working_directory_abspath):
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
