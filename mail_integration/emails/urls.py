from django.urls import path
from . import views

urlpatterns = [
    path('email-form/', views.get_email_account, name='email_form'),
    path('messages/', views.message_list, name='message_list'),
]
