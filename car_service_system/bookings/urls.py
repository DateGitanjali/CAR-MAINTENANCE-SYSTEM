from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/', views.book_service, name='book_service'),
    path('book/<int:garage_id>/', views.book_service, name='book_service_garage'),
    path('list/', views.booking_list, name='booking_list'),
    path('detail/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('invoice/<int:pk>/', views.download_invoice, name='download_invoice'),
]
