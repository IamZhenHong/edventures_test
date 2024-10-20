from django.urls import path
from .views import ChatbotResponseView, AddDocumentsView, add_document
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('query/', ChatbotResponseView.as_view(), name='chatbot-response'),
    path('add-document_template/', add_document, name='add-document'),
    path('add-document/', AddDocumentsView.as_view(), name='add-document'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
