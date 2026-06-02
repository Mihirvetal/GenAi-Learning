from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex
from dotenv import load_dotenv
import os

load_dotenv()
# Force Python to ignore the broken SSL path
os.environ.pop("SSL_CERT_FILE", None)
def main(url: str) -> None: 
    # Read the webpage
    document = SimpleWebPageReader(html_to_text=True).load_data(urls=[url])
    
    # Create the index
    index = VectorStoreIndex.from_documents(documents=document)
    
    # Query the index
    query_engine = index.as_query_engine()
    response = query_engine.query("who is michael?")
    
    print(response)

if __name__ == "__main__":
    main(url="https://en.wikipedia.org/wiki/Prison_Break")