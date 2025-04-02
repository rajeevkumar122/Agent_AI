# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# import uvicorn
# import faiss
# import json
# import os
# import logging
# import google.generativeai as genai
# from sentence_transformers import SentenceTransformer

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize FastAPI app
# app = FastAPI()

# #  Enable CORS for frontend communication
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# #  API Key for Gemini AI (Replace with your actual key)
# API_KEY = "AIzaSyAuof-veYPuBB9bplKO-54A0PIgG0Mjkdo"
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel("gemini-1.5-pro")

# #  Constants
# DATA_DIR = r"C:\Users\rajee\Desktop\Agent_AI\fronted\Data"
# VECTOR_DB_PATH = os.path.join(DATA_DIR, "vector_database.index")
# STRUCTURED_DATA_PATH = os.path.join(DATA_DIR, "structured_data.json")
# RELEVANCE_THRESHOLD = 1.5
# TOP_K_RESULTS = 3

# #  Load FAISS index
# try:
#     index = faiss.read_index(VECTOR_DB_PATH)
#     logging.info("FAISS index loaded successfully!")
# except Exception as e:
#     logging.error(f"Error loading FAISS index: {str(e)}")
#     raise e

# #  Load structured data
# try:
#     with open(STRUCTURED_DATA_PATH, "r", encoding="utf-8") as f:
#         structured_data = json.load(f)
#     logging.info(f"Loaded {len(structured_data)} structured text chunks!")
# except Exception as e:
#     logging.error(f"Error loading structured data: {str(e)}")
#     raise e

# #  Load SentenceTransformer model
# try:
#     embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
#     logging.info("Embedding model loaded successfully!")
# except Exception as e:
#     logging.error(f"Error loading embedding model: {str(e)}")
#     raise e

# #  Request Model
# class QueryRequest(BaseModel):
#     query: str

# #  FAISS Search Function
# def search_faiss(query, top_k=TOP_K_RESULTS):
#     try:
#         query_vector = embedding_model.encode(query, convert_to_tensor=True).cpu().numpy().reshape(1, -1)
#         distances, indices = index.search(query_vector, top_k)
#         valid_indices = [idx for idx in indices[0] if 0 <= idx < len(structured_data)]
#         retrieved_chunks = [structured_data[idx] for idx in valid_indices]
        
#         if not retrieved_chunks or distances[0][0] > RELEVANCE_THRESHOLD:
#             return "Out of context", []
#         return "Relevant", retrieved_chunks
#     except Exception as e:
#         logging.error(f"FAISS search error: {str(e)}")
#         return "Error", []

# #  Endpoint for AI-based query
# @app.post("/ask")
# def post_ask(request: QueryRequest):
#     try:
#         status, retrieved_chunks = search_faiss(request.query)
        
#         if status == "Out of context":
#             return {
#                 "response": "I cannot answer that based on the provided information.",
#                 "sources": []
#             }

#         # Convert sources into structured button format
#         sources = [{"file_link": chunk["file_link"], "title": f"Source {i+1}"} for i, chunk in enumerate(retrieved_chunks)]

#         # Generate AI response
#         prompt = f"""
#         You are an AI assistant. Based on the following retrieved information, answer the query:

#         {retrieved_chunks}

#         Question: {request.query}

#         Provide a well-structured response and include relevant source links at the end.
#         """
#         response = model.generate_content(prompt)

#         # Prepare structured response
#         response_data = {
#             "response": response.text,
#             "sources": sources  # Now structured as objects for frontend buttons
#         }

#         return response_data
#     except Exception as e:
#         logging.error(f"Error processing request: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import uvicorn
# import faiss
# import json
# import os
# import logging
# import requests
# from sentence_transformers import SentenceTransformer

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize FastAPI app
# app = FastAPI()

# # Enable CORS for frontend communication
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # API Key for Hanooman API (Replace with your actual key)
# API_KEY = "akm5535x-m60d44cc-39dbca60-fccb8d59"
# ENDPOINT_URL ="https://api.us.inc/hanooman/router/v1/chat/completions"

# # Constants
# DATA_DIR = r"C:\Users\rajee\Desktop\Agent_AI\fronted\Data"
# VECTOR_DB_PATH = os.path.join(DATA_DIR, "vector_database.index")
# STRUCTURED_DATA_PATH = os.path.join(DATA_DIR, "structured_data.json")
# RELEVANCE_THRESHOLD = 1.42  # Updated threshold
# TOP_K_RESULTS = 3

# # Load FAISS index
# try:
#     index = faiss.read_index(VECTOR_DB_PATH)
#     logging.info("FAISS index loaded successfully!")
# except Exception as e:
#     logging.error(f"Error loading FAISS index: {str(e)}")
#     raise e

# # Load structured data
# try:
#     with open(STRUCTURED_DATA_PATH, "r", encoding="utf-8") as f:
#         structured_data = json.load(f)
#     logging.info(f"Loaded {len(structured_data)} structured text chunks!")
# except Exception as e:
#     logging.error(f"Error loading structured data: {str(e)}")
#     raise e

# # Load SentenceTransformer model
# try:
#     embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
#     logging.info("Embedding model loaded successfully!")
# except Exception as e:
#     logging.error(f"Error loading embedding model: {str(e)}")
#     raise e

# # Request Model
# class QueryRequest(BaseModel):
#     query: str

# # FAISS Search Function
# def search_faiss(query, top_k=TOP_K_RESULTS):
#     try:
#         query_vector = embedding_model.encode(query, convert_to_tensor=True).cpu().numpy().reshape(1, -1)
#         distances, indices = index.search(query_vector, top_k)
#         valid_indices = [idx for idx in indices[0] if 0 <= idx < len(structured_data)]
#         retrieved_chunks = [structured_data[idx] for idx in valid_indices]
        
#         if not retrieved_chunks or distances[0][0] > RELEVANCE_THRESHOLD:
#             return "Out of context", []
#         return "Relevant", retrieved_chunks
#     except Exception as e:
#         logging.error(f"FAISS search error: {str(e)}")
#         return "Error", []

# # Function to interact with Hanooman API
# def generate_hanooman_response(prompt):
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {API_KEY}",
#     }
    
#     payload = {
#         "messages": [
#             {"role": "system", "content": "You are an AI assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         "model": "everest",  # Replace with correct model name
#         "max_tokens": 524,  # Added max_tokens to increase token limit for full response
#     }
    
#     try:
#         response = requests.post(ENDPOINT_URL, headers=headers, json=payload)
#         response.raise_for_status()  # Raise an error for bad status codes
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Error interacting with Hanooman API: {str(e)}")
#         return None

# # Endpoint for AI-based query
# @app.post("/ask")
# def post_ask(request: QueryRequest):
#     try:
#         status, retrieved_chunks = search_faiss(request.query)
        
#         if status == "Out of context":
#             return {
#                 "response": "I cannot answer that based on the provided information.",
#                 "sources": []
#             }

#         # Convert sources into structured button format
#         sources = [{"file_link": chunk["file_link"], "title": f"Source {i+1}"} for i, chunk in enumerate(retrieved_chunks)]

#         # Generate AI response
#         prompt = f"""
#         You are an AI assistant. Based on the following retrieved information, answer the query:

#         {retrieved_chunks}

#         Question: {request.query}

#         Provide a well-structured full response and include relevant source links at the end.
#         """
        
#         hanooman_response = generate_hanooman_response(prompt)

#         if hanooman_response is None:
#             raise HTTPException(status_code=500, detail="Error generating response from Hanooman API")

#         # Check if the response contains source links (if available)
#         sources_from_ai = []
#         if 'sources' in hanooman_response:
#             sources_from_ai = hanooman_response['sources']  # Assuming sources are in 'sources' key

#         # Prepare structured response
#         response_data = {
#             "response": hanooman_response.get("choices")[0].get("message").get("content"),
#             "sources": sources + sources_from_ai  # Combine sources from retrieved chunks and AI response
#         }

#         return response_data
#     except Exception as e:
#         logging.error(f"Error processing request: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import faiss
import json
import os
import logging
import requests
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key for Hanooman API (Replace with your actual key)
API_KEY = "akm5535x-m60d44cc-39dbca60-fccb8d59"
ENDPOINT_URL = "https://api.us.inc/hanooman/router/v1/chat/completions"

# Constants
DATA_DIR = r"C:\Users\rajee\Desktop\Agent_AI\fronted\Data"
VECTOR_DB_PATH = os.path.join(DATA_DIR, "vector_database.index")
STRUCTURED_DATA_PATH = os.path.join(DATA_DIR, "structured_data.json")
RELEVANCE_THRESHOLD = 1.42  # Updated threshold
TOP_K_RESULTS = 3

# Load FAISS index
try:
    index = faiss.read_index(VECTOR_DB_PATH)
    logging.info("✅ FAISS index loaded successfully!")
except Exception as e:
    logging.error(f"❌ Error loading FAISS index: {str(e)}")
    raise e

# Load structured data
try:
    with open(STRUCTURED_DATA_PATH, "r", encoding="utf-8") as f:
        structured_data = json.load(f)
    logging.info(f"✅ Loaded {len(structured_data)} structured text chunks!")
except Exception as e:
    logging.error(f"❌ Error loading structured data: {str(e)}")
    raise e

# Load SentenceTransformer model
try:
    embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    logging.info("✅ Embedding model loaded successfully!")
except Exception as e:
    logging.error(f"❌ Error loading embedding model: {str(e)}")
    raise e

# Request Model
class QueryRequest(BaseModel):
    query: str

# FAISS Search Function
def search_faiss(query, top_k=TOP_K_RESULTS):
    try:
        query_vector = embedding_model.encode(query, convert_to_tensor=True).cpu().numpy().reshape(1, -1)
        distances, indices = index.search(query_vector, top_k)
        valid_indices = [idx for idx in indices[0] if 0 <= idx < len(structured_data)]
        retrieved_chunks = [structured_data[idx] for idx in valid_indices]
        
        if not retrieved_chunks or distances[0][0] > RELEVANCE_THRESHOLD:
            return "Out of context", []
        return "Relevant", retrieved_chunks
    except Exception as e:
        logging.error(f"❌ FAISS search error: {str(e)}")
        return "Error", []

# Function to interact with Hanooman API
def generate_hanooman_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "model": "everest",  # Replace with correct model name
        "max_tokens": 524,  # Added max_tokens to increase token limit for full response
    }
    
    try:
        response = requests.post(ENDPOINT_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error interacting with Hanooman API: {str(e)}")
        return None

# Endpoint for AI-based query
@app.post("/ask")
def post_ask(request: QueryRequest):
    try:
        status, retrieved_chunks = search_faiss(request.query)
        
        if status == "Out of context":
            return {
                "response": "I cannot answer that based on the provided information.",
                "sources": []
            }

        # Convert sources into structured button format
       # Convert sources into structured button format (without count in title)
        sources = [{"file_link": chunk["file_link"], "title": "Source"} for chunk in retrieved_chunks]


        # Generate AI response
        prompt = f"""
        You are an AI assistant. Based on the following retrieved information, answer the query:

        {retrieved_chunks}

        Question: {request.query}

        Provide a well-structured full response and include relevant source links at the end.
        """
        
        hanooman_response = generate_hanooman_response(prompt)

        if hanooman_response is None:
            raise HTTPException(status_code=500, detail="Error generating response from Hanooman API")

        # Extract sources from AI response
        sources_from_ai = []
        if 'sources' in hanooman_response:
            sources_from_ai = hanooman_response['sources']  # Assuming sources are in 'sources' key

        # Combine sources and remove duplicates
        all_sources = sources + sources_from_ai
        unique_sources = {src["file_link"]: src for src in all_sources}.values()  # Remove duplicates based on 'file_link'

        # Prepare structured response
        response_data = {
            "response": hanooman_response.get("choices")[0].get("message").get("content"),
            "sources": list(unique_sources)  # Convert back to a list
        }

        return response_data
    except Exception as e:
        logging.error(f"❌ Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
