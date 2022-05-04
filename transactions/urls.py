from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transactions import views


app_name = 'transaction'

router = DefaultRouter()
router.register(r'transactions', views.TransactionViewSet)
