from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.garage_dashboard, name='garage_dashboard'),
    path('profile/', views.garage_profile, name='garage_profile'),
    path('add-service/', views.add_service, name='add_service'),
    path('delete-service/<int:pk>/', views.delete_service, name='delete_service'),
]