import os
from dotenv import load_dotenv
# ========== LANGCHAIN ==========
# LANGCHAIN: Vector database for semantic search
from langchain_community.vectorstores import FAISS
# LANGCHAIN: OpenAI embeddings - converts text to vectors
from langchain_openai import OpenAIEmbeddings
# LANGCHAIN: Text chunking utility
from langchain_text_splitters import CharacterTextSplitter
# LANGCHAIN: Document loader for text files
from langchain_community.document_loaders import TextLoader
# ==============================

# Load environment variables from .env file (specify path relative to parent directory)
from pathlib import Path
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def rag_agent(state):
    docs_path = "data/knowledge_docs"
    if not os.path.isdir(docs_path) or not os.listdir(docs_path):
        state["rag_insight"] = "No knowledge documents found."
        return state

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        state["rag_insight"] = "RAG agent: Searching knowledge base... (API key required for embeddings)"
        return state
    
    try:
        # ========== LANGCHAIN ==========
        # LANGCHAIN: Create embeddings using OpenAI API
        embeddings = OpenAIEmbeddings(api_key=api_key)
        # ==============================
        docs = []
        
        for file in os.listdir(docs_path):
            if file.endswith(".txt"):
                # ========== LANGCHAIN ==========
                # LANGCHAIN: Load text files using TextLoader
                loader = TextLoader(os.path.join(docs_path, file))
                # ==============================
                docs.extend(loader.load())

        # ========== LANGCHAIN ==========
        # LANGCHAIN: Split documents into chunks (500 chars, 50 overlap)
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        # LANGCHAIN: Create FAISS vector database from chunks
        db = FAISS.from_documents(chunks, embeddings)
        # LANGCHAIN: Perform semantic similarity search
        results = db.similarity_search("sales decline reasons", k=1)
        # ==============================
        
        state["rag_insight"] = results[0].page_content if results else "No specific insights found."
    except Exception as e:
        state["rag_insight"] = f"RAG Search: {str(e)[:200]}"
    
    return state
