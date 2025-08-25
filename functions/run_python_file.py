import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Execute Python files with optional arguments in the specified directory relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

        if not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_target_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        


        result = subprocess.run(
        ["python3", abs_target_path], 
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text=True,
        timeout=30,
        cwd=abs_working_dir
        )
        #formatting
        output = []
        output.append(f"STDOUT:\n{result.stdout}")
        output.append(f"STDERR:\n{result.stderr}")


        #cases
        if result.stdout == "" and result.stderr == "" and result.returncode == 0:
             return "No output produced."
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"