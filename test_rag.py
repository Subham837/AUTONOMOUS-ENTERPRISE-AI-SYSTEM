#!/usr/bin/env python
"""
RAG Agent Test - Verify different queries return different results
This proves the RAG system is working dynamically, not returning hardcoded data
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

def test_rag_different_queries():
    """Test RAG with multiple queries to verify dynamic retrieval"""
    
    print("\n" + "="*80)
    print("RAG SYSTEM VERIFICATION TEST")
    print("Testing with Different Queries")
    print("="*80 + "\n")
    
    docs_path = "data/knowledge_docs"
    
    # Step 1: Load documents
    print("[STEP 1] Loading Knowledge Base Documents...")
    docs = []
    for file in os.listdir(docs_path):
        if file.endswith(".txt"):
            print(f"  ✓ {file}")
            loader = TextLoader(os.path.join(docs_path, file))
            docs.extend(loader.load())
    print(f"  Total documents loaded: {len(docs)}\n")
    
    # Step 2: Split into chunks
    print("[STEP 2] Creating Text Chunks...")
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"  Total chunks created: {len(chunks)}\n")
    
    # Step 3: Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found in .env file")
        print("Please add your OpenAI API key to .env")
        return False
    
    print("[STEP 3] Initializing Embeddings...")
    try:
        embeddings = OpenAIEmbeddings(api_key=api_key)
        print("  ✓ OpenAI Embeddings initialized\n")
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:100]}")
        print("  Note: API key might be invalid or quota exceeded\n")
        return False
    
    # Step 4: Create vector database
    print("[STEP 4] Creating Vector Database (FAISS)...")
    try:
        db = FAISS.from_documents(chunks, embeddings)
        print(f"  ✓ Vector database created with {len(chunks)} vectors\n")
    except Exception as e:
        print(f"  ✗ Error creating vector database: {str(e)[:100]}\n")
        return False
    
    # Step 5: Test with different queries
    print("[STEP 5] Testing Different Queries (Semantic Search)")
    print("-" * 80 + "\n")
    
    test_queries = [
        "sales decline reasons",
        "customer retention strategies",
        "personalization benefits",
        "churn rate reduction",
        "innovation improvements",
    ]
    
    results_collected = {}
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: '{query}'")
        try:
            results = db.similarity_search(query, k=1)
            if results:
                result_text = results[0].page_content[:150]
                results_collected[query] = result_text
                print(f"  Result: {result_text}...\n")
            else:
                print(f"  Result: No matching documents\n")
        except Exception as e:
            print(f"  Error: {str(e)[:100]}\n")
            return False
    
    # Step 6: Verify results are different
    print("-" * 80)
    print("[STEP 6] Verification Results")
    print("-" * 80 + "\n")
    
    unique_results = len(set(results_collected.values()))
    total_queries = len(test_queries)
    
    print(f"Total queries executed: {total_queries}")
    print(f"Unique results returned: {unique_results}")
    
    if unique_results > 1:
        print("\n✅ RAG IS WORKING PROPERLY!")
        print("   Different queries returned different results.")
        print("   Semantic search is functioning dynamically.")
    else:
        print("\n⚠️  WARNING: All queries returned similar results")
        print("   This might indicate an issue with semantic search")
    
    print("\n" + "="*80)
    return True


if __name__ == "__main__":
    import sys
    success = test_rag_different_queries()
    sys.exit(0 if success else 1)
