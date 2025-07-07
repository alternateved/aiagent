import os


def issubdir(subdirectory, directory):
    directory_abspath = os.path.abspath(directory)
    subdirectory_abspath = os.path.abspath(subdirectory)
    return subdirectory_abspath.startswith(directory_abspath)
