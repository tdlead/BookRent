from django.urls import path
from .views import BookTitleListView, book_title_detail_view
# main path name
app_name = 'books'

urlpatterns = [
    #name main for reference
     path('', BookTitleListView.as_view(), {'letter':None}, name='main'),
     path('<str:letter>/', BookTitleListView.as_view(), name='main'),
     path('<pk>/',book_title_detail_view, name='detail'),
]
