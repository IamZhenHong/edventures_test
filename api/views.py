from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.document_retriever import find_relevant_document
from .services.pdf_processing import pdf_processing
from .services.csv_processing import csv_processing

class ChatbotResponseView(APIView):
    """
    View to handle queries to the chatbot and return responses.
    """

    def post(self, request):
        """Handle POST requests to get chatbot responses."""
        user_input = request.data.get('query')
        if not user_input:
            return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Process the query and return the response
            response = self.query_processing(user_input)
            return Response({"response": response}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def query_processing(self, user_input):
        """Process the user query, find relevant documents, and return the response."""

        # Find the relevant document
        document = find_relevant_document(user_input)
        
        if document is None:
            raise ValueError("No relevant document found.")

        # Process the document based on its file type
        if document.file_type == 'pdf':
            response = pdf_processing(document, user_input)
        elif document.file_type == 'csv':
            response = csv_processing(document, user_input)
        else:
            raise ValueError("Unsupported document type.")

        return response