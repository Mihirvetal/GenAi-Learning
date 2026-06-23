from haystack import Pipeline
from haystack.components.converters.pypdf import PyPDFToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack_integrations.document_stores.pinecone import PineconeDocumentStore
from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from haystack.utils import Secret



def run_ingestion(file_path: str):
    # 1. Initialize Pinecone Document Store
    # document_store = PineconeDocumentStore(
    #     api_key=PINECONE_API_KEY,
    #     index=PINECONE_INDEX_NAME,
    #     dimension=384 # Dimension matches 'all-MiniLM-L6-v2'
    # )
    document_store = PineconeDocumentStore(
        api_key=Secret.from_token(PINECONE_API_KEY), # <-- WRAPPED IN SECRET
        index=PINECONE_INDEX_NAME, 
        dimension=384 
    )

    # 2. Instantiate Components
    converter = PyPDFToDocument()
    splitter = DocumentSplitter(split_by="word", split_length=200, split_overlap=30)
    embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")

    # 3. Build Haystack 2.0 Ingestion Pipeline
    pipeline = Pipeline()
    pipeline.add_component("converter", converter)
    pipeline.add_component("splitter", splitter)
    pipeline.add_component("embedder", embedder)

    # Connect nodes sequentially
    pipeline.connect("converter", "splitter")
    pipeline.connect("splitter", "embedder")

    # 4. Execute and write to Document Store
    print(f"Starting ingestion for: {file_path}")
    result = pipeline.run({"converter": {"sources": [file_path]}})
    
    # Write embedded documents directly to Pinecone
    documents = result["embedder"]["documents"]
    document_store.write_documents(documents)
    print("Ingestion successfully completed!")

if __name__ == "__main__":
    # Test block to run directly: python -m src.ingestion
    import sys
    if len(sys.argv) > 1:
        run_ingestion(sys.argv[1])