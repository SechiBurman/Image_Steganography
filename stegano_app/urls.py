from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('about/', views.about, name='about'),
    path('download-encrypted-image/', views.download_encrypted_image, name='download_encrypted_image'),
    path('encryption/', views.encryption_view, name='encryption'),
    path('decryption/', views.decryption_view, name='decryption')
]