import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

_ = load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    if len(sys.argv) < 3:
        print("Usage: uv run main.py <working_directory> <prompt> [--verbose]")
        sys.exit(1)

    working_directory = sys.argv[1]
    verbose = len(sys.argv) > 3 and sys.argv[2] == "--verbose"
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[2])]),
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    for _ in range(0, 20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            if not response.function_calls and response.text:
                print(response.text)
                break

            if response.candidates:
                for candidate in response.candidates:
                    if content := candidate.content:
                        messages.append(content)

            if response.function_calls:
                for function_call in response.function_calls:
                    result = call_function(working_directory, function_call, verbose)

                    if (
                        result is not None
                        and result.parts
                        and result.parts[0].function_response is not None
                        and result.parts[0].function_response.name is not None
                        and result.parts[0].function_response.response is not None
                    ):
                        content = types.Content(
                            role="tool",
                            parts=[
                                types.Part.from_function_response(
                                    name=result.parts[0].function_response.name,
                                    response=result.parts[0].function_response.response,
                                )
                            ],
                        )

                        messages.append(content)

                        if verbose:
                            print(f"-> {result.parts[0].function_response.response}")
                    else:
                        raise Exception("invalid response")

        except Exception as e:
            print(f"unexpected error: {e}")


if __name__ == "__main__":
    main()
