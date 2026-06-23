from haystack import Pipeline, component
from haystack.components.builders import PromptBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from pinecone import Pinecone
from haystack import Document
from google import genai  
from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME, GEMINI_API_KEY

# 1. NATIVE PINECONE RETRIEVER COMPONENT WITH NAMESPACE ALIGNMENT
@component
class CustomPineconeRetriever:
    def __init__(self, api_key: str, index_name: str):
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(index_name)

    @component.output_types(documents=list)
    def run(self, query_embedding: list[float], top_k: int = 5):
        # Explicitly hitting the "default" namespace created by haystack
        response = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            namespace="default"  # <-- CRITICAL ADDITION
        )
        
        matches = response.get("matches", [])
        print(f"\n🔍 [DEBUG] Pinecone returned {len(matches)} matches from 'default' namespace.")
        
        docs = []
        for i, match in enumerate(matches):
            metadata = match.get("metadata", {}) 
            content = metadata.get("content") or metadata.get("text") or ""
            docs.append(Document(content=content, meta=metadata, score=match.get("score")))
        return {"documents": docs}


# 2. NATIVE GEMINI GENERATOR COMPONENT
@component
class CustomGeminiGenerator:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    @component.output_types(replies=list)
    def run(self, prompt: str):
        print("\n🚀 [DEBUG] EXACT PROMPT SENT TO GEMINI:")
        print("=" * 60)
        print(prompt.strip())
        print("=" * 60)
        
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return {"replies": [response.text]}


def create_rag_pipeline():
    template = """
    You are a helpful assistant. Answer the question based strictly on the provided context.
    If the answer cannot be found in the context, say 'I do not have enough information to answer.'
    
    Context:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}
    
    Question: {{ query }}
    Answer:
    """

    text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
    retriever = CustomPineconeRetriever(api_key=PINECONE_API_KEY, index_name=PINECONE_INDEX_NAME)
    prompt_builder = PromptBuilder(template=template, required_variables=["documents", "query"])
    generator = CustomGeminiGenerator(api_key=GEMINI_API_KEY)

    rag = Pipeline()
    rag.add_component("text_embedder", text_embedder)
    rag.add_component("retriever", retriever)
    rag.add_component("prompt_builder", prompt_builder)
    rag.add_component("generator", generator)

    rag.connect("text_embedder.embedding", "retriever.query_embedding")
    rag.connect("retriever.documents", "prompt_builder.documents")
    rag.connect("prompt_builder.prompt", "generator.prompt")

    return rag

def query_rag(query_text: str):
    pipeline = create_rag_pipeline()
    response = pipeline.run({
        "text_embedder": {"text": query_text},
        "prompt_builder": {"query": query_text}
    })
    return response["generator"]["replies"][0]