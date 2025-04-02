import os
import json
import fitz  # PyMuPDF
import pandas as pd
import numpy as np
import faiss
import logging
from urllib.parse import quote, urljoin
from sentence_transformers import SentenceTransformer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text.strip() if text else None
    except Exception as e:
        logging.error(f"Error processing PDF {pdf_path}: {e}")
        return None

# Function to extract text from CSV
def extract_text_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path, dtype=str, encoding="utf-8-sig", errors="replace")
        text = "\n".join(df.apply(lambda x: ' '.join(x.dropna()), axis=1))
        return text.strip() if text else None
    except Exception as e:
        logging.error(f"Error processing CSV {csv_path}: {e}")
        return None

# Function to extract text from Excel
def extract_text_from_excel(excel_path):
    try:
        df = pd.read_excel(excel_path, dtype=str)
        text = "\n".join(df.apply(lambda x: ' '.join(x.dropna()), axis=1))
        return text.strip() if text else None
    except Exception as e:
        logging.error(f"Error processing Excel {excel_path}: {e}")
        return None

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i: i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Function to generate dataset link
def generate_dataset_link(file_name, file_path, use_cloud=False):
    base_url = "https://your-cloud-storage.com/datasets/" if use_cloud else "file://"
    return urljoin(base_url, quote(file_name)) if use_cloud else f"file:///{quote(os.path.abspath(file_path))}"

# Define data directory
data_dir = r"C:\Users\rajee\Desktop\Agent_AI\fronted\Data"

if not os.path.isdir(data_dir):
    raise FileNotFoundError(f"Data directory not found: {data_dir}")

all_files = os.listdir(data_dir)
logging.info(f"Found {len(all_files)} files in data directory.")

structured_data = []

for file in all_files:
    file_path = os.path.join(data_dir, file)
    text, file_type = None, None
    
    if file.lower().endswith(".pdf"):
        logging.info(f"Processing PDF: {file}")
        text = extract_text_from_pdf(file_path)
        file_type = "PDF"
    elif file.lower().endswith(".csv"):
        logging.info(f"Processing CSV: {file}")
        text = extract_text_from_csv(file_path)
        file_type = "CSV"
    elif file.lower().endswith(".xlsx"):
        logging.info(f"Processing Excel: {file}")
        text = extract_text_from_excel(file_path)
        file_type = "Excel"
    else:
        logging.warning(f"Skipping unsupported file type: {file}")
        continue
    
    if not text:
        logging.warning(f"Skipping empty or unreadable file: {file}")
        continue
    
    chunks = split_text_into_chunks(text, chunk_size=500)
    dataset_link = generate_dataset_link(file, file_path, use_cloud=False)
    
    for i, chunk in enumerate(chunks):
        structured_data.append({
            "file_name": file,
            "file_type": file_type,
            "file_link": dataset_link,
            "chunk_index": i,
            "text_chunk": chunk
        })

if not structured_data:
    raise ValueError("No valid text chunks found! Ensure files contain readable text.")

logging.info(f"Processed {len(set(d['file_name'] for d in structured_data))} files and stored {len(structured_data)} text chunks.")

with open("structured_data.json", "w", encoding="utf-8") as json_file:
    json.dump(structured_data, json_file, indent=4, ensure_ascii=False)

# Compute embeddings
batch_size = 32
embeddings = np.vstack([embedding_model.encode([d["text_chunk"]]) for d in structured_data]).astype("float32")

dimension = embeddings.shape[1]
index_file = "vector_database.index"

if os.path.exists(index_file):
    logging.info("Loading existing FAISS index...")
    index = faiss.read_index(index_file)
else:
    logging.info("Creating new FAISS index...")
    index = faiss.IndexFlatL2(dimension)

index.add(embeddings)
faiss.write_index(index, index_file)
logging.info(f"Successfully stored {len(structured_data)} text chunks!")

# Load structured data
def search_faiss(query, top_k=5):
    query_embedding = embedding_model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    results = [{
        "file_name": structured_data[i]["file_name"],
        "file_type": structured_data[i]["file_type"],
        "file_link": structured_data[i]["file_link"],
        "chunk_index": structured_data[i]["chunk_index"],
        "text_chunk": structured_data[i]["text_chunk"],
        "score": round(float(distances[0][list(indices[0]).index(i)]), 4)
    } for i in indices[0] if i < len(structured_data)]
    return sorted(results, key=lambda x: x["score"], reverse=True)

if __name__ == "__main__":
    query = "What is the impact of cardiovascular diseases?"
    results = search_faiss(query, top_k=3)
    logging.info("Search Results:")
    for res in results:
        logging.info(f"{res['file_name']} (Chunk {res['chunk_index']}): {res['text_chunk'][:200]}... Score: {res['score']}")