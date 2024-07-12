from django.urls import path
from .views import search_book_view

app_name = 'rentals'

urlpatterns = [
    path('', search_book_view, name='main')
]
