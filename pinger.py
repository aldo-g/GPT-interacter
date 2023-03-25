import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

def ping_openai_api():
    try:
        models = openai.Model.list()
        return True
    except Exception as e:
        print("Error:", e)
        return False

print(ping_openai_api())