from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Product, ShoppingCart, User, Category, Color, Size, CartItem


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords must match!')
        return data

    def validate_email(self, data):
        query = get_user_model().objects.filter(email__iexact=data)
        if query.exists():
            raise serializers.ValidationError('User with this email already exists!')
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email']
        )     
        user.set_password(validated_data['password'])
        user.save()
        return user


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['size']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    color = ColorSerializer(many=True, read_only=True)
    size = SizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'color', 'size', 'price', 'image']

    # def validate(self, attrs):
    #     if attrs.get('category') == ''

class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cart_item):
        return cart_item.quantity * cart_item.product.price


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    product_size = serializers.ChoiceField(choices=Size.SIZE_CHOICES)
    product_color = serializers.ChoiceField(choices=Color.COLOR_CHOICES) 

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity', 'product_size', 'product_color']

    def validate(self, data):
        product_id = data.get('product_id')
        size = data.get('product_size')
        color = data.get('product_color')
        product = Product.objects.get(pk=product_id)
        # print(size, type(size))
        # print(color, type(color))
        # print(product, type(product))
        # print(product.size.all())
        if not any([size == str(s) for s in product.size.all()]):
            raise serializers.ValidationError('Нет выбранного размера.')
        if not any([color == str(c) for c in product.color.all()]):
            raise serializers.ValidationError('Нет выбранного цвета.')
        if not str(product.category) == Category.HATS and size == Size.UNDEFINED:
            raise serializers.ValidationError('Необходимо указать размер')
        # print(product.category, type(product.category))
        return data

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Нет такого продукта.')
        return value

    def validate_quantity(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Количество товара должно быть от 1 до 10.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        size = self.validated_data['product_size']
        color = self.validated_data['product_color']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id, size=size, color=color)
            cart_item.quantity += quantity
            if cart_item.quantity > 10:
                raise serializers.ValidationError('Количество товара должно быть от 1 до 10.')
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, product_id=product_id, size=size, color=color, quantity=quantity)
        self.instance = cart_item
        return self.instance


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    # customer = serializers.StringRelatedField()
    class Meta:
        model = ShoppingCart
        fields = ['id', 'customer', 'items', 'total_price']

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])


class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'date_joined', 'username']
