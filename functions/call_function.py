from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file


def call_function(
    working_directory: str,
    function_call_part: types.FunctionCall,
    verbose: bool = False,
) -> types.Content | None:
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_call_part.name:
        if function_call_part.name not in functions:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={
                            "error": f"Unknown function: {function_call_part.name}"
                        },
                    )
                ],
            )

        kwargs = function_call_part.args.copy() if function_call_part.args else {}
        kwargs["working_directory"] = working_directory
        function_result = functions[function_call_part.name](**kwargs)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )
