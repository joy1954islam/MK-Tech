from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('registration', views.CustomerRegisterViewSet, basename='customer_registration')

router.register('login', views.UserLoginViewSet, basename='login')

router.register('product-search', views.ProductSearchViewSet, basename='product_search')

router.register('admin-view-all-customer-list', views.AllCustomerListViewSet, basename='admin_view_all_customer_list')

router.register('order-create', views.CreateOrderViewSet, basename='order_create')
router.register('order-status-change', views.OrderStatusChangeViewSet, basename='order_status_change')

urlpatterns = [
    # API view Route
    path('api/', include(router.urls)),

]
