from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    path('vehicle/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicle/edit/<int:pk>/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicle/delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),
    path('search/', views.search_garage, name='search_garages'),
    path('bookings/', views.booking_history, name='booking_history'),
]
