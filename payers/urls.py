from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payers import views

app_name = 'payer'

router = DefaultRouter()
router.register(r'payers', views.PayerViewSet)
