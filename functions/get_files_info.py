import os


def get_files_info(working_directory: str, directory: str | None = None) -> str:
    full_path = os.path.join(working_directory, directory or ".")
    working_directory_abspath = os.path.abspath(working_directory)
    full_path_abspath = os.path.abspath(full_path)

    if not full_path_abspath.startswith(working_directory_abspath):
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

    except Exception as e:
        return f"Error: {e}"

    return "\n".join(result)
