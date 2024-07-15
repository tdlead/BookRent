from django.urls import path
from .views import search_book_view, BookRentalView, UpdateRentalStatus, CreateNewRental, SelectRentalDownloandView

app_name = 'rentals'

urlpatterns = [
    path('', search_book_view, name='main'),
    path('<str:book_id>/', BookRentalView.as_view(), name='detail' ),
    path('new/<str:book_id>/', CreateNewRental.as_view(), name='new'),
    path('<str:book_id>/<pk>/', UpdateRentalStatus.as_view(), name='update' ),
    path('download/<str:book_id>', SelectRentalDownloandView.as_view(), name='download' ),
]
