import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("api key is None")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    print("Hello from ai-agent!")

    for _ in range(20):
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages,
            tools=available_functions,
        )
        usage = response.usage
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            if usage is not None:
                prompt_tokens  = usage.prompt_tokens
                print(f"Prompt tokens: {prompt_tokens}")
                completion_tokens = usage.completion_tokens
                print(f"Response tokens: {completion_tokens}")
            else: 
                raise RuntimeError("usage is empty")
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if result_message.get("content") == "":
                    raise Exception("content is null")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            print(message.content)
            return
    print("The agent reached the 20-iteration limit without a final response")
    sys.exit(1)

if __name__ == "__main__":
    main()
