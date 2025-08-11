

import chromadb
import wikipedia
import ollama

# Load the ChromaDB
client = chromadb.PersistentClient(path="./chroma_db_free")

# Assume there's at least one collection; take the first one
collections = client.list_collections()
if not collections:
    raise ValueError("No collections found in the ChromaDB.")
collection = collections[0]  # Or specify the name, e.g., client.get_collection("your_collection_name")

def retrieve_from_chroma(query, n_results=5):
    """Retrieve relevant chunks from ChromaDB."""
    results = collection.query(query_texts=[query], n_results=n_results)
    documents = results['documents'][0] if results['documents'] else []
    return documents

def retrieve_from_wikipedia(query, num_results=3):
    """Retrieve summaries from Wikipedia."""
    query_wiki = f"{query} kerala laws"
    search_results = wikipedia.search(query_wiki, results=num_results)
    summaries = []
    for result in search_results:
        try:
            page = wikipedia.page(result)
            summaries.append(page.summary[:1000])  # Limit to 1000 chars
        except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
            pass
    return summaries

def generate_answer(question, model_name="llama3.1:latest"):
    """Generate answer using RAG with prompt engineering via Ollama."""
    # Retrieve from ChromaDB
    chroma_docs = retrieve_from_chroma(question)
    chroma_context = "\n\n".join(chroma_docs) if chroma_docs else "No relevant information found in the database."

    # Retrieve from Wikipedia
    wiki_summaries = retrieve_from_wikipedia(question)
    wiki_context = "\n\n".join(wiki_summaries) if wiki_summaries else "No relevant Wikipedia information found."

    # Combine contexts
    full_context = f"Database Context:\n{chroma_context}\n\nWikipedia Context:\n{wiki_context}"

    # Prompt engineering
    prompt = f"""You are a knowledgeable legal assistant specialising in kerala law. Answer the question accurately and concisely based ONLY on the provided context from our database and Wikipedia(only use information in wikipedia regarding kerala laws). Do not use external knowledge or make up information. If the context lacks sufficient information, state: "I don't have enough information to answer this question."

Provide your answer in this format:
- **Answer**: [Your direct answer]
- **Reasoning**: [Explanation based on context]
- **Sources**: [Cite specific parts of the context]

Context:
{full_context}

Question: {question}"""

    # Query the local Ollama model
    try:
        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500
            }
        )
        generated_text = response['response'].strip()
        return generated_text
    except Exception as e:
        raise ValueError(f"Ollama request failed: {str(e)}")

# Main loop for user input
if __name__ == "__main__":
    print("Welcome to the RAG system with Ollama. Enter your question (type 'exit' to quit).")
    
    # Debug: Print model list
    try:
        model_list = ollama.list()['models']
        available_models = [getattr(m, 'model', 'Unknown') for m in model_list]
        print("Available Ollama models:", available_models)
        # Debug: Print raw model attributes
        print("Raw model attributes:")
        for m in model_list:
            print(f"  - Model: {getattr(m, 'model', 'Unknown')}, ID: {getattr(m, 'digest', 'Unknown')}")
    except Exception as e:
        print(f"Error fetching model list: {str(e)}")
        available_models = []

    if not available_models or all(m == 'Unknown' for m in available_models):
        print("No models available or model list is invalid. Please install a model using 'ollama pull <model_name>' (e.g., 'ollama pull llama3.1').")
        exit(1)

    model_name = input("Enter the Ollama model to use (e.g., llama3.1:latest, or press Enter for default 'llama3.1:latest'): ").strip() or "llama3.1:latest"
    try:
        # Normalize model name: Accept 'llama3.1' and convert to 'llama3.1:latest'
        if model_name == "llama3.1" and "llama3.1:latest" in available_models:
            model_name = "llama3.1:latest"
        # Verify model exists
        if model_name not in available_models:
            raise ValueError(f"Model {model_name} not found. Available models: {available_models}")
        
        while True:
            question = input("Question: ").strip()
            if question.lower() == 'exit':
                break
            if not question:
                continue
            try:
                answer = generate_answer(question, model_name)
                print("\nAnswer:\n", answer, "\n")
            except Exception as e:
                print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
