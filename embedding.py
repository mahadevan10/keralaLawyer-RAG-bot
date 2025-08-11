import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb

# --- Configuration ---
input_text_file = "combined_legal_text_for_rag.txt"
chroma_db_directory = "./chroma_db_free"  # Directory to store ChromaDB data
chunk_size = 500  # Number of characters per chunk
chunk_overlap = 100  # Overlap between chunks (helps maintain context)
batch_size = 5000  # Number of embeddings to process at once

# --- Main Processing ---
def process_text_for_rag_free_api(text_file, db_directory, chunk_size, chunk_overlap, batch_size):
    """
    Reads a text file, chunks the content, embeds the chunks using a free Hugging Face model,
    and stores them in ChromaDB.
    """
    print(f"Loading text from: {text_file}")
    with open(text_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 1. Chunk the text
    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    docs = text_splitter.create_documents([raw_text])
    print(f"Created {len(docs)} chunks.")

    # 2. Encode the chunks (create embeddings) and store in ChromaDB
    print("Generating embeddings using Hugging Face model and storing in ChromaDB (in batches)...")
    
    # Initialize Hugging Face Embeddings model (free)
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5") # 1.1.2

    # Initialize ChromaDB connection (persistent client)
    # Data will be automatically persisted to `db_directory` as chunks are added.
    vectorstore = Chroma(persist_directory=db_directory, embedding_function=embeddings) # 1.1.2, 1.2.13

    # Process in batches
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i : i + batch_size]
        print(f"Processing batch {i//batch_size + 1}/{len(docs)//batch_size + 1} ({len(batch_docs)} chunks)")
        vectorstore.add_documents(documents=batch_docs) # 1.1.2
    
    # No need to call vectorstore.persist() here anymore!
    print(f"Embeddings and chunks stored in ChromaDB at {db_directory}")

# Run the function
process_text_for_rag_free_api(input_text_file, chroma_db_directory, chunk_size, chunk_overlap, batch_size)
