# authentication/urls.py
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('verify-email/<str:uidb64>/<str:token>/',
         views.EmailVerificationView.as_view(), name='verify-email'),
    path('check-email/', views.EmailCheckView.as_view(), name='check-email'),
    path('check-password/', views.PasswordCheckView.as_view(), name='check-password'),
]
