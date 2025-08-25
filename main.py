import sys
import os
from google import genai
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.call_function import call_function

from prompts import system_prompt
from call_function import available_functions  # or wherever you defined it

from prompts import system_prompt
from call_function import available_functions  # or wherever you defined it


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    conversation = []
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}\n")
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for turn in range(20):
        response = generate_content(client, messages, verbose)
        if response.text and not response.function_calls:  # Only stop if there's text AND no function calls
            print("Final response:")
            print(response.text)
            break

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        ),
    )
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    # Add LLM response to messages
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # Handle function calls
    function_responses = []
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            function_responses.append(function_call_result.parts[0])
    
    if function_responses:  # Only add if we actually have responses
        messages.append(types.Content(role="user", parts=function_responses))
    
    return response  # This should be at the function level, not inside the if!

if __name__ == "__main__":
    main()
