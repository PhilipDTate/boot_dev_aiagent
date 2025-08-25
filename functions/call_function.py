from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
import os
from google.genai import types

def call_function(function_call_part, verbose=False):
    function_name=function_call_part.name
    working_directory = "./calculator"
    function_call_part.args["working_directory"]=working_directory

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})") 
    else:
        print(f" - Calling function: {function_call_part.name}") 

    function_dict = {
        "write_file": write_file,
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
    }

    if function_call_part.name in function_dict:

        function_result = function_dict[function_call_part.name](**function_call_part.args)

        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
            )
        ],
        )
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
    )