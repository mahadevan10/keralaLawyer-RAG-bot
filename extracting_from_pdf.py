import fitz  # PyMuPDF module
import glob
import os

pdf_directory = r"C:\Users\hp\keralaLawyer\pdfs"  # Replace with your actual directory path
output_text_file = "combined_legal_text_for_rag.txt"

def extract_text_from_pdf_for_rag(pdf_path):
    """Extracts text from a single PDF, minimizing separators for RAG."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            # Extract text with minimal processing for chunking
            # get_text() with default options works well for RAG, {Link: according to Medium https://medium.com/@pymupdf/rag-llm-and-pdf-conversion-to-markdown-text-with-pymupdf-03af00259b5d}
            text += page.get_text() # No extra newline here, the chunking mechanism will handle spacing
        doc.close()
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}") # 1.1.8
    return text

def process_pdfs_to_single_text_file_for_rag(pdf_folder, output_file):
    """Processes all PDFs in a folder and saves the combined text to a single file for RAG."""
    all_extracted_text = ""
    pdf_files = glob.glob(os.path.join(pdf_folder, '*.pdf')) # 1.6.2

    if not pdf_files:
        print(f"No PDF files found in {pdf_folder}")
        return

    for pdf_file in pdf_files:
        print(f"Extracting text from: {pdf_file}")
        extracted_text = extract_text_from_pdf_for_rag(pdf_file)
        # You might add a small, consistent separator here if you want to distinguish between documents
        # For instance, a unique ID or file path, {Link: according to GitHub https://github.com/pymupdf/RAG}
        all_extracted_text += extracted_text

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_extracted_text)
    print(f"All extracted text saved to {output_file}")

# Run the function
process_pdfs_to_single_text_file_for_rag(pdf_directory, output_text_file)
