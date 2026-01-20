import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv

load_dotenv()

def rag_agent(state):
    docs_path = "data/knowledge_docs"
    if not os.listdir(docs_path):
        state["rag_insight"] = "No knowledge documents found."
        return state

    embeddings = OpenAIEmbeddings() # Requires OPENAI_API_KEY in .env
    docs = []
    
    for file in os.listdir(docs_path):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(docs_path, file))
            docs.extend(loader.load())

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    db = FAISS.from_documents(chunks, embeddings)
    results = db.similarity_search("sales decline reasons", k=1)
    
    state["rag_insight"] = results[0].page_content if results else "No specific insights found."
    return state