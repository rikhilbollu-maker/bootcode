import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        valid_dir_2 = os.path.isdir(target_dir)
        if not valid_dir_2:
            return f'Error: "{directory}" is not a directory'
        files_info = []
        for name in os.listdir(target_dir):
            info_path = os.path.join(target_dir, name)
            file_size = os.path.getsize(info_path)
            dir = os.path.isdir(info_path)
            files_info.append(f"- {name}: file_size={file_size} bytes, is_dir={dir}")
        return "\n".join(files_info)
    except Exception as e:
        return (f"Error: Something went wrong: {e}")

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
