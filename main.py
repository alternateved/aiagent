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
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <prompt> [--verbose]")
        sys.exit(1)

    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
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
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.function_calls:
        for function_call in response.function_calls:
            result = call_function(function_call, verbose)

            if (
                result is not None
                and result.parts
                and result.parts[0].function_response is not None
                and result.parts[0].function_response.response is not None
            ):
                if verbose:
                    print(f"-> {result.parts[0].function_response.response}")
            else:
                raise Exception("invalid response")

    if verbose:
        print(f"User prompt: {sys.argv[1]}")
        if usage := response.usage_metadata:
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")


if __name__ == "__main__":
    main()
