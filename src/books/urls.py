from django.urls import path
from .views import BookTitleListView, BookListView, BookTitleDetailView
# main path name
app_name = 'books'

urlpatterns = [
    #name main for reference
     path('', BookTitleListView.as_view(), {'letter':None}, name='main'),
     path('<str:letter>/', BookTitleListView.as_view(), name='main'),
     path('<str:letter>/<slug>/', BookTitleDetailView.as_view(), name='detail'),
]
