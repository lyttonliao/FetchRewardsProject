from django.urls import path, include
from transactions import views


app_name = 'transaction'


urlpatterns = [
    path('transactions/', views.TransactionsList.as_view()),
    path('transactions/<int:pk>/', views.TransactionDetail.as_view())
]
