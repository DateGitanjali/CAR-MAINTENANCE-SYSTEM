from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.customer_dashboard, name='dashboard'),

    # Vehicle management
    path('vehicle/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicle/edit/<int:pk>/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicle/delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),

    # Garage search + detail
    path('search/', views.search_garage, name='search_garages'),
    path('garage/<int:garage_id>/', views.garage_detail, name='garage_detail'),

    # Booking history
    path('bookings/', views.booking_history, name='booking_history'),

    # Reviews / feedback
    path('garage/<int:garage_id>/review/', views.add_review, name='add_review'),
]
