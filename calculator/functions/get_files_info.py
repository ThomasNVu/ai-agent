import os

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


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        direct = os.path.abspath(
            working_directory
        )  # Converts directory to absolute for reliability
        joined = os.path.join(
            direct, directory
        )  # Combines working directory with directory to get ex: ../folder/file.py
        target_dir = os.path.normpath(joined)  # Cleans up path by removing . and ..

        valid_target_dir = os.path.commonpath([direct, target_dir]) == direct
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):  # Ensures path is a direcotry and not a file
            return f'Error: "{directory}" is not a directory'

        print(f'Success: "{directory}" is within the working directory')
        result = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(
                target_dir, item
            )  # Get's the rest of the items from filepath
            file_size = os.path.getsize(item_path)  # Check for size
            is_dir = os.path.isdir(item_path)  # Check if the filepath is there
            result.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(result)

    except Exception as e:
        return f"Error listing files: {e}"
