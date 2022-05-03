from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users import views

app_name = 'user'

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]