import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from .embedder import create_embeddings
from ..models import Document


# Assuming documents is defined globally or fetched inside the function as needed
documents = Document.objects.all()


def find_relevant_document(query):
    """
    Find the most relevant document based on a query.
    """

    query_embedding = create_embeddings(query) # Make sure to implement this or use OpenAI API directly
    
    titles = []
    embeddings = []

    # Generate embeddings for each document title
    for document in documents:
        title_embedding = create_embeddings(document.title)
        titles.append(document.title)
        embeddings.append(title_embedding)

    # Compute cosine similarities between the query embedding and each document embedding
    similarities = cosine_similarity([query_embedding], embeddings).flatten()

    # Find the index of the document with the highest similarity score
    most_similar_index = int(similarities.argmax())

    return documents[most_similar_index]