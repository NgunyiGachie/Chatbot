import openai
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_gpt(prompt, model="gpt-4o-mini"):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
            )
            response_text = response['choices'][0]['message']['content']
            return response_text
        except openai.error.RateLimitError:
            if attempt < max_retries - 1:
                print("Rate limit hit, sleeping for 20 seconds...")
                time.sleep(20)
            else:
                print("Max retries reached. Please check your API quota.")
                return None
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            return None

def generate_json(prompt, response, filename="response.json"):
    data = {
        "prompt": prompt,
        "response": response
    }
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    prompt = "Explain how to use Flask with SQLAlchemy"
    total_requests = 0
    daily_limit = 200
    rpm_limit = 3
    sleep_time = 60 / rpm_limit

    while total_requests < daily_limit:
        response_text = chat_gpt(prompt)
        if response_text:
            generate_json(prompt, response_text)
            total_requests += 1
            print(f"Request {total_requests} saved to JSON file.")
            time.sleep(sleep_time)
        else:
            break

if __name__ == "__main__":
    main()
