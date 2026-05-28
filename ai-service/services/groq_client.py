import os
from pathlib import Path
from services.config import (
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS
)

import time
from groq import Groq
from dotenv import load_dotenv

# load env variables safely
env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)


# get api key
api_key = os.getenv("GROQ_API_KEY")

# initialize groq client
client = Groq(api_key=api_key)


def generate_response(prompt):

    retries = 3

    for attempt in range(retries):

        try:

            start_time = time.time()

            response = client.chat.completions.create(
                model=MODEL_NAME,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )

            end_time = time.time()

            print(
                f"AI Response Time: {end_time - start_time:.2f} seconds"
            )

            content = response.choices[0].message.content

            if not content:
                raise Exception("Empty AI response")

            return content

        except Exception as e:

            print(f"Retry {attempt + 1} failed")
            print(str(e))

            time.sleep(1)

    return None