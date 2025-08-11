# KeralaLawyer — AI-Powered Legal Assistant for Kerala State Laws

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()

---

## Overview

**KeralaLawyer** is a cutting-edge Retrieval-Augmented Generation (RAG) system built to assist legal professionals, researchers, and citizens by providing precise, context-aware answers about Kerala state laws. Leveraging modern AI techniques combined with domain-specific legal data, this project demonstrates expertise in web scraping, NLP, embeddings, vector search, and local LLM deployment.

The system efficiently scrapes official legal PDFs, extracts and processes legal texts, generates semantic embeddings, and utilizes a locally hosted LLaMA model (via Ollama) to answer complex legal queries in natural language.

---

## Why KeralaLawyer?

- **Democratizing Legal Access:** Makes complex Kerala laws easily accessible via natural language queries.
- **End-to-End Automation:** From data scraping to answer generation, the entire pipeline is automated and runs locally, ensuring privacy and control.
- **Technological Depth:** Combines web scraping, document processing, semantic search, and LLMs — showcasing proficiency in full-stack AI development.
- **Real-World Application:** Tackles real legal domain challenges, including multi-format document processing, vector database indexing, and context-aware generation.

---

## Core Components & Technologies

| Component              | Technology/Tool              | Role                                                        |
|------------------------|------------------------------|-------------------------------------------------------------|
| Data Acquisition       | Python, `playwright`         | Scrape Kerala laws PDFs from official IndiaCode website.    |
| Text Extraction        | `PyMuPDF`                    | Extract text accurately from multi-page PDF documents.      |
| Embeddings Generation  | `sentence-transformers`      | Convert legal text into semantic vector embeddings.         |
| Vector Database        | `ChromaDB`                   | Store embeddings for fast, similarity-based retrieval.      |
| Language Model         | LLaMA (local) via `Ollama`   | Generate coherent, context-aware answers to user queries.   |
| Query System           | Python                       | Orchestrate retrieval + generation for the RAG pipeline.    |

---

## Project Workflow

1. **Web Scraping & PDF Download**

   - Targeted scraping of Kerala-specific legal documents from [IndiaCode](https://www.indiacode.nic.in/).
   - Automated batch download of all relevant PDFs ensuring comprehensive legal coverage.

2. **Text Extraction & Preprocessing**

   - Extract text from complex PDFs maintaining structural integrity using `PyMuPDF`.
   - Merge and clean extracted texts into a unified corpus optimized for embedding.

3. **Embedding & Vectorization**

   - Utilize a pre-trained sentence transformer model (`all-MiniLM-L6-v2`) to generate embeddings.
   - Persist embeddings in a local `ChromaDB` vector store for efficient semantic search.

4. **Retrieval-Augmented Generation (RAG)**

   - Upon user query, retrieve relevant legal text chunks from `ChromaDB`.
   - Feed retrieved context into the locally hosted LLaMA model (via Ollama) for natural language answer generation.

## Installation & Usage


# Clone the repo
git clone https://github.com/yourusername/KeralaLawyer.git
cd KeralaLawyer

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate    # Linux/macOS
# OR
.\venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run scraper to download PDFs(Optional)

# Generate embeddings and build vector store
python src/embedding.py

# Start interactive RAG query system
python src/rag_script_ollama.py

## Example

(rag-gpu) PS C:\Users\hp\keralaLawyer> & C:/Users/hp/miniconda3/envs/rag-gpu/python.exe c:/Users/hp/keralaLawyer/rag_script_ollama.py
Welcome to the RAG system with Ollama. Enter your question (type 'exit' to quit).
Available Ollama models: ['llama3.1:latest']
Raw model attributes:
  - Model: llama3.1:latest
Enter the Ollama model to use (e.g., llama3.1:latest, or press Enter for default 'llama3.1:latest'):
Question: can i drive without helmet

Answer:
 **Answer**: No
**Reasoning**: According to Kerala law, no motor vehicle liable to tax under section 3 shall be kept for use in the State unless a valid tax licence obtained. Additionally, there is no specific information provided in the context regarding helmet usage, but based on general knowledge and Wikipedia Context, it is common that wearing helmets while driving is mandatory in India.
**Sources**: [None mentioned specifically from provided context]

## Licenses

MIT License

Copyright (c) 2025 Mahadevan Biju Menon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[...standard MIT License text...]

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


# Disclaimer

The KeralaLawyer project(this repo) is an experimental AI-based system designed to provide information regarding Kerala state laws.

**Important:**

- The answers generated by this system are based on automated retrieval and language model generation techniques.
- It is **not** a substitute for professional legal advice.
- The author does **not** guarantee the accuracy, completeness, or reliability of any information provided by this system.
- Use the system at your own risk.
- Under no circumstances shall the author be held liable for any direct, indirect, incidental, special, consequential, or punitive damages arising out of the use or inability to use this software or the information generated.

For any legal matters, always consult a qualified legal professional.

---

By using this software, you agree to these terms.
