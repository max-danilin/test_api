from django.urls import path, include
from rest_framework_nested import routers
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('carts', views.CartViewSet, basename='carts')

cartitem_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cartitem_router.register('items', views.CartItemViewSet, basename='cart_item')


urlpatterns = [
    path('login/', views.MyObtainTokenPairView.as_view(), name='token'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
urlpatterns += router.urls + cartitem_router.urls
