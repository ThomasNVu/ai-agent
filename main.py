import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json
import sys

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("Environment not loaded")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    generate_content(client, messages, args.verbose)


def generate_content(client: OpenAI, messages: list, verbose: bool = False) -> None:
    for _ in range(20):
        response = call_model(client, messages)
        message = response.choices[0].message
        if not response.usage:
            raise RuntimeError("API response appears to be malformed")
        if verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose)
                # function_args = json.loads(tool_call.function.arguments or "{}") # type: ignore
                # print(f"Calling function: {tool_call.function.name}({function_args})") # type: ignore
                messages.append(result_message)
                if result_message["content"] == "":
                    raise Exception("This is empty")
                if verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(message.content)
            break
    else:
        print("Agent didn't finish within the maximum number of iterations")
        sys.exit(1)


def call_model(client, messages):
    return client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions, # type: ignore
    )


if __name__ == "__main__":
    main()
