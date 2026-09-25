import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs  = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        valid_dir = os.path.isdir(target_dir)
        if valid_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(target_dir)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(target_dir, "w") as x:
            x.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



    except Exception as e:
        return f"Error: Something went wrong: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes and/or overwrites files in a specified directory relative to the working directory.",
        "parameters": {
            "type": "object",
            "required": ["file_path","content"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the file to write/overwrite, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the file",
                },
            },
        },
    },
}
