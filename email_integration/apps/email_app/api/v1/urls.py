from django.urls import path

from .views import HelloWorldView, RegisterSuperUserView, EmailMessageListView

urlpatterns = [
    path('hello/', HelloWorldView.as_view(), name='hello_email_app'),
    path('register/', RegisterSuperUserView.as_view(), name='register_superuser'),
    path('email-messages/', EmailMessageListView.as_view(), name='email-message-list'),
]
