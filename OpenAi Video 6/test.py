# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# print(repr(api_key))

# client = OpenAI(api_key=api_key)

# try:
#     models = client.models.list()
#     print("API Key is working")
# except Exception as e:
#     print("Error:", e)


# working with ollama
from llama_index.llms.ollama import Ollama

llm = Ollama(
    model="llama3",
    request_timeout=300.0
)

response = llm.complete("Who is salman khan?")

print(response.text)