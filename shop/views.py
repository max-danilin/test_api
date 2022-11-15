from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, ShoppingCart, User, CartItem
from .serializers import ProductSerializer, CartSerializer, CustomerSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, MyTokenObtainPairSerializer, UserRegisterSerializer, AddCartSerializer
from .filters import ProductFilter, CustomerFilter
from .permissions import IsAdminOrReadOnly, CartPermission

# Create your views here.
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({'access': str(token.access_token), 'refresh': str(token)})


class ProductViewSet(RetrieveModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    # queryset = Product.objects.select_related('category').select_related('size').select_related('color').all()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price']
    permission_classes = [IsAdminOrReadOnly]

    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = ShoppingCart.objects.prefetch_related('items__product').all()
    # serializer_class = CartSerializer
    permission_classes = [CartPermission]

    def get_serializer_context(self):
        return {'user': self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartSerializer
        return CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


class CustomerViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CustomerFilter
    search_fields = ['username']
    ordering_fields = ['date_joined']

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]