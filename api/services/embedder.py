import os

from dotenv import load_dotenv
import openai
from langchain_openai.embeddings import OpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()

# Access the variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key for OpenAI is not set.")

def create_embeddings(text):
    embed_model = OpenAIEmbeddings(openai_api_key=api_key)

    # Ensure the text length is within the allowed limit
    if len(text) > 4096:  # Adjust based on the model's limit
        text = text[:4096]  # Truncate or handle as needed

    # Create embeddings for the text 
    embedding = embed_model.embed_query(text)  
    return embedding