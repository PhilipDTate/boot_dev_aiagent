import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Reads the file contents of the specified file, relative to the working directory. If not provided, reads from the working directory itself.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

        if not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        MAX_CHARS = 10000

        with open(abs_target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    
        if len(file_content_string) == MAX_CHARS:
            return f"{file_content_string} [...File \"{file_path}\" truncated at 10000 characters]"
    
        return f"{file_content_string}"
    except Exception as e:
        return f"Error: {e}"