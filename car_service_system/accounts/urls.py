from django.urls import path
from . import views

app_name = 'accounts' 

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('select-role/', views.select_role, name='select_role'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password/verify/', views.forgot_password_verify, name='forgot_password_verify'),
    path('forgot-password/resend/', views.resend_reset_otp, name='resend_reset_otp'),
    path('forgot-password/reset/', views.forgot_password_reset, name='forgot_password_reset'),
    path('password/change/', views.change_password, name='change_password'),
]