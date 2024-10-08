from django.urls import path
from .views import ChatbotResponseView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('query/', ChatbotResponseView.as_view(), name='chatbot-response'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)