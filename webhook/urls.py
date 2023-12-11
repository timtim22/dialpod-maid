from django.urls import path
from . import views

urlpatterns = [
    # ... other paths ...
    path('dialpad-webhook/', views.dialpad_webhook, name='dialpad-webhook'),
]