from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.email_app.api.v1.urls'))
]
