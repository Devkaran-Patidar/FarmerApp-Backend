
from django.urls import path
from . import views
urlpatterns = [
    path('chatboat/',views.chat_api),
]
