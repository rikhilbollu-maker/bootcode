import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        valid_file = os.path.isfile(target_dir)
        if not valid_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout = 30)
        output_string = []
        if result.returncode != 0:
            output_string.append(f'Process exited with code {result.returncode}')
        if not result.stdout and not result.stderr:
            output_string.append("No output produced")
        if result.stdout:
            output_string.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_string.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output_string)
        



    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a Python file in the working directory.",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The relative path to the Python file to execute.",
                },
                "args": {
                    "type": "array",
                    "description": "Optional command-line arguments to pass to the script",
                    "items": {
                        "type": "string",
                    },
                },
            },
        },
    },
}
