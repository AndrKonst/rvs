from django.urls import path

from .views import increment, clear_db

urlpatterns = [
    path('<slug:num>', increment),
    path('clear/', clear_db),
]
