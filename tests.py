from functions.write_file import write_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

print("Tests for get_files_info")
directories = [".", "pkg", "/bin"]
for directory in directories:
    result = get_files_info("calculator", directory)
    print(f"Result for {directory} directory:")
    print(result)
    print("\n")

print("Tests for get_file_content")
files = ["lorem.txt", "main.py", "pkg/calculator.py", "/bin/cat"]
for file in files:
    result = get_file_content("calculator", file)
    print(f"Result for {file} file:")
    print(result)
    print("\n")

print("Tests for write_file")
tuples = [
    ("lorem.txt", "wait, this isn't lorem ipsum"),
    ("pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("/tmp/temp.txt", "this should not be allowed"),
]
for tuple in tuples:
    result = write_file("calculator", tuple[0], tuple[1])
    print(f"Result for {tuple[0]} file:")
    print(result)
    print("\n")
