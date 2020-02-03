from django.urls import path

from .views import increment, clear_db

urlpatterns = [
    path('', increment),
    path('clear/', clear_db),
]
