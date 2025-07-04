from functions.get_files_info import get_files_info

directories = [".", "pkg", "/bin"]

for directory in directories:
    result = get_files_info("calculator", directory)
    print(f"Result for {directory} directory:")
    print(result)
