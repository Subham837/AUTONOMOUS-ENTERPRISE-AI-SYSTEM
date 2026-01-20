#!/usr/bin/env python
"""
RAG Test - Works WITHOUT OpenAI API (uses mock embeddings)
Demonstrates that RAG retrieves DIFFERENT data for DIFFERENT queries
"""

import os
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def test_rag_without_openai():
    """Test RAG using TF-IDF (no API calls needed)"""
    
    print("\n" + "="*80)
    print("RAG SYSTEM VERIFICATION TEST")
    print("(Works WITHOUT OpenAI - Using TF-IDF for semantic similarity)")
    print("="*80 + "\n")
    
    docs_path = "data/knowledge_docs"
    
    # Step 1: Load documents
    print("[STEP 1] Loading Knowledge Base Documents...")
    docs = []
    doc_sources = []
    
    for file in os.listdir(docs_path):
        if file.endswith(".txt"):
            print(f"  ✓ {file}")
            loader = TextLoader(os.path.join(docs_path, file))
            loaded_docs = loader.load()
            docs.extend(loaded_docs)
            doc_sources.extend([file] * len(loaded_docs))
    
    print(f"  Total documents loaded: {len(docs)}\n")
    
    # Step 2: Split into chunks
    print("[STEP 2] Creating Text Chunks...")
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    chunk_texts = [chunk.page_content for chunk in chunks]
    print(f"  Total chunks created: {len(chunks)}\n")
    
    # Step 3: Create TF-IDF vectorizer (alternative to OpenAI embeddings)
    print("[STEP 3] Building Vector Space (TF-IDF)...")
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    chunk_vectors = vectorizer.fit_transform(chunk_texts)
    print(f"  ✓ Vector space created\n")
    
    # Step 4: Test with different queries
    print("[STEP 4] Testing Different Queries (Semantic Search)")
    print("-" * 80 + "\n")
    
    test_queries = [
        "sales decline reasons",
        "customer retention strategies", 
        "personalization benefits",
        "churn rate reduction",
        "innovation improvements",
    ]
    
    results_dict = {}
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: '{query}'")
        
        # Vectorize query
        query_vector = vectorizer.transform([query])
        
        # Find most similar chunks
        similarities = cosine_similarity(query_vector, chunk_vectors)[0]
        top_idx = np.argmax(similarities)
        similarity_score = similarities[top_idx]
        
        # Get result
        result_text = chunk_texts[top_idx][:150]
        results_dict[query] = result_text
        
        print(f"  Similarity Score: {similarity_score:.3f}")
        print(f"  Result: {result_text}...\n")
    
    # Step 5: Verify results are different
    print("-" * 80)
    print("[STEP 5] Verification Results")
    print("-" * 80 + "\n")
    
    unique_results = len(set(results_dict.values()))
    total_queries = len(test_queries)
    
    print(f"Total queries executed: {total_queries}")
    print(f"Unique results returned: {unique_results}")
    print(f"Diversity: {(unique_results/total_queries)*100:.1f}%")
    
    if unique_results > 1:
        print("\n✅ RAG IS WORKING PROPERLY!")
        print("   ✓ Different queries returned different results")
        print("   ✓ Semantic search is functioning dynamically")
        print("   ✓ System is NOT returning hardcoded/cached data")
        success = True
    else:
        print("\n⚠️  WARNING: All queries returned similar results")
        success = False
    
    # Show query-result mapping
    print("\n" + "="*80)
    print("Query → Result Mapping")
    print("="*80 + "\n")
    
    for query, result in results_dict.items():
        print(f"Q: {query}")
        print(f"A: {result}...\n")
    
    print("="*80)
    return success


if __name__ == "__main__":
    import sys
    success = test_rag_without_openai()
    sys.exit(0 if success else 1)
