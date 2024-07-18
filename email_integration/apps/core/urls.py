from django.urls import path, include
from .views import HelloWorldView


urlpatterns = [
    path('core/hello', HelloWorldView.as_view(), name='core'),
    path('email_app/', include('apps.email_app.urls'))
]
