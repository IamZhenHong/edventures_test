from django.urls import path
from .views import ChatbotResponseView, AddDocumentsView, add_document, ListDocumentsView, DeleteDocumentView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('query/', ChatbotResponseView.as_view(), name='chatbot-response'),
    path('add-document/', AddDocumentsView.as_view(), name='add-document'),
    path('list_documents/', ListDocumentsView.as_view(), name='list-documents'),
    path('delete_document/', DeleteDocumentView.as_view(), name='delete-document'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
