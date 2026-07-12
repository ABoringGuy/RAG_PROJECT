from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate(prompt):
    try:
        response= client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role":"user",
                     "content":prompt
                }
            ],
            temperature=0.1,
        )

        return response.choices[0].message.content

    except Exception as e:
        error = str(e).lower()

        if "context" in error or "token" in error or "maximum context length" in error:
            return {
                "status": "token_limit",
                "message": "Token is exceeded for the day"
            }

        raise