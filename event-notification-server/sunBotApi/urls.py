from django.urls import path
from . import views


urlpatterns = [
    path('request', views.Gateway.as_view())
]