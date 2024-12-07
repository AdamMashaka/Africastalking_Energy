from django.urls import path
from . import views

urlpatterns = [
    path('sms/', views.sms_webhook, name='sms_webhook'),
]
