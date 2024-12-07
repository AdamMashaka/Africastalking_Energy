# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ensure this line is present
    path('sms/', views.sms_webhook, name='sms_webhook'),
    path('bulb-status/', views.bulb_status, name='bulb_status'),
    path('toggle-bulb/', views.toggle_bulb, name='toggle_bulb'),
]