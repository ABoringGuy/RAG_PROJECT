from dotenv import load_dotenv
from groq import Groq, RateLimitError
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate(prompt):
    MODELS= ["llama-3.3-70b-versatile",
             "llama-3.1-8b-instant"]
    last_exception = None
    for model in MODELS:
        try:
            response= client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role":"user",
                         "content":prompt
                    }
                ],
                temperature=0.1,
            )
            return response.choices[0].message.content

        except RateLimitError as e:
            last_exception = e
            continue
    raise last_exception