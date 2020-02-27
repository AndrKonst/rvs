from django.urls import path

from .views import increment, clear_db, curl

urlpatterns = [
    path('', increment),
    path('clear/', clear_db),
    path('curl/', curl)
]
