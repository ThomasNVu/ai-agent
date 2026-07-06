import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        direct = os.path.abspath(working_directory)
        joined = os.path.join(direct, directory)
        target_dir = os.path.normpath(joined)

        valid_target_dir = os.path.commonpath([direct, target_dir]) == direct
    except:
        return "Error: Standard library isn't working"
    if not valid_target_dir:
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(target_dir):
        return(f'Error: "{directory}" is not a directory')
    else:
        return f'Success: "{directory}" is within the working directory'