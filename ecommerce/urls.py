from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('registration', views.CustomerRegisterViewSet, basename='customer_registration')

router.register('login', views.UserLoginViewSet, basename='login')

urlpatterns = [
    # API view Route
    path('api/', include(router.urls)),

]
