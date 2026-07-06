import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
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
    messages=[
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    if args.verbose:
        print(f'User prompt: {args.user_prompt}\n')

    generate_content(client, messages, args.verbose)


def generate_content(client: OpenAI, messages: list, verbose: bool = False) -> None:
    response = client.chat.completions.create(model='openrouter/free', messages=messages)
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")
    if verbose:
        print(f'Prompt tokens: {response.usage.prompt_tokens}')
        print(f'Response tokens: {response.usage.completion_tokens}')

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
