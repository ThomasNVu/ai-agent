import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        direct = os.path.abspath(
            working_directory
        )  # Converts directory to absolute for reliability
        joined = os.path.join(
            direct, file_path
        )  # Combines working directory with directory to get ex: ../folder/file.py
        target_dir = os.path.normpath(joined)  # Cleans up path by removing . and ..

        valid_target_dir = os.path.commonpath([direct, target_dir]) == direct
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):  # Ensures path is a direcotry and not a file
            return f'Error: "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)

        with open(target_dir, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

        print(f'Success: "{file_path}" is within the working directory')

    except Exception as e:
        return f"Error listing files: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}