import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        direct = os.path.abspath(working_directory)
        joined = os.path.join(direct, file_path)
        target_dir = os.path.normpath(joined)

        valid_target_dir = os.path.commonpath([direct, target_dir]) == direct
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if os.path.splitext(file_path)[1] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args:
            command.extend(args)

        complete_object = subprocess.run(
            args=command, capture_output=True, text=True, timeout=30
        )
        exit_message = ""
        if complete_object.returncode != 0:
            exit_message = exit_message + (
                f"Process exited with code {complete_object.returncode}\n"
            )
        if not complete_object.stdout and not complete_object.stderr:
            exit_message += "No output produced"
        else:
            exit_message += (
                f"STDOUT: {complete_object.stdout}\nSTDERR: {complete_object.stderr}"
            )
        return exit_message
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}