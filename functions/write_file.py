import os


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    working_directory_abspath = os.path.abspath(working_directory)
    full_path_abspath = os.path.abspath(full_path)

    if not full_path_abspath.startswith(working_directory_abspath):
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
