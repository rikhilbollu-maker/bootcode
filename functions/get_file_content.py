from config import MAX_CHARS
import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        valid_file_path = os.path.isfile(target_dir)
        if not valid_file_path:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_dir) as x:
            file_content = x.read(MAX_CHARS)
            if x.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content
            else:
                return file_content
    except Exception as e:
        return f"Error: File content could not be read: {e}"

