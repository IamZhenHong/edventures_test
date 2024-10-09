import os
import requests
from dotenv import load_dotenv

import openai
from openai import OpenAI 
from transformers import pipeline

from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from django.conf import settings

# Load environment variables from .env file
load_dotenv()


# Access the variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("API key for OpenAI is not set.")
CHROMA_PATH = '.chromadb'
client = OpenAI(api_key=openai_api_key)


def pdf_processing(document, query):

    # Process and store the PDF embeddings
    process_and_store_pdf_embeddings(document.file_name)

    # Check if the Chroma database exists
    try:
        embed_model = OpenAIEmbeddings(openai_api_key = openai_api_key)
        semantic_chunk_vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embed_model)
        print("Chroma vectorstore registered successfully.")

    except Exception as e:
        print(f"Failed to register Chroma vectorstore: {str(e)}")
        return None  
    
    # Uncomment this block of code to see the chunk lengths for the document
    # # Retrieve all chunks stored in the Chroma vector store
    # print("All chunks and their lengths in the database:")
    # all_chunks = semantic_chunk_vectorstore._collection.get(include=['documents'])  # Access the internal collection

    # # if 'documents' in all_chunks:
    # #     for idx, chunk in enumerate(all_chunks['documents']):
    # #         chunk_length = len(chunk)  # Assuming each document is a string
    # #         print(f"Chunk {idx+1}: Length = {chunk_length}")
    # # else:
    # #     print("No chunks found in the database.")


    # Create a retriever for semantic chunks from the vector store, configured to return the top 1 result based on the search query.
    semantic_chunk_retriever = semantic_chunk_vectorstore.as_retriever(search_kwargs={"k":3})

    # Execute the query to retrieve most relevant chunks
    result = semantic_chunk_retriever.invoke(query)

    if not result:
        print("No results found for the query.")
        return None  # Handle the error appropriately
    
    # Augment the retrieved chunks with the query
    augmented_result = augment_chunk(result, query, document.title)
    

    # for idx, chunk in enumerate(result):
    #     print(f"Chunk {idx+1}: {chunk}")
    # print("Augmented result:")
    # print(augmented_result)

    # Return the retrieved chunks
    return augmented_result

def process_and_store_pdf_embeddings(file_name):

    # Initialize the embedding model
    embed_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

    pdf_path = os.path.join(settings.MEDIA_ROOT, 'documents', file_name)

    # Check if the Chroma database already exists
    if os.path.exists(CHROMA_PATH):
        print("Loading existing Chroma vectorstore from disk...")
        # Load the existing Chroma vectorstore from the directory
        semantic_chunk_vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embed_model)
    else:
        print("Creating new Chroma vectorstore...")
        # Initialize Chroma for new vectorstore
        semantic_chunk_vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embed_model)

        # Load your PDF document
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # Initialize the Semantic Chunker
        semantic_chunker = SemanticChunker(embed_model, breakpoint_threshold_type="percentile")

        # Create semantic chunks from the document contents
        document_contents = [d.page_content for d in documents]

        # Create semantic chunks without progress bar
        semantic_chunks = []
        for page_number, content in enumerate(document_contents, start=1):
            chunks = semantic_chunker.create_documents([content])
            
            # Add page number to each chunk's metadata
            for chunk in chunks:
                chunk.metadata = {"page_number": page_number}  # Add the current page number to metadata

            semantic_chunks.extend(chunks)

        # Add new embeddings to the existing vectorstore
        print("Adding new embeddings to the vectorstore...")
        semantic_chunk_vectorstore.add_documents(semantic_chunks)

        # Save the vectorstore to disk
        semantic_chunk_vectorstore.persist()
        print("New embeddings added and vectorstore saved.")


# Function to augment chunks and query using OpenAI API
def augment_chunk(chunks, user_query, title):
    if not chunks or len(chunks) == 0:
        print("No chunks available for augmentation.")
        return None  # Handle the error appropriately

    # Prepare the content to be passed in the messages array
    prompt = (
        f"This information is derived from the document titled: '{title}'.\n\n"
        f"Given the following information extracted:\n\n"
        f"{chunks}\n\n"
        f"Here is the query: '{user_query}'.\n\n"
        f"Please combine the text with the query to create a clear, concise answer based only on the information provided. "
        f"Do not add external information or expand beyond what's necessary."
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that synthesizes a response given a query and a search result."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message 