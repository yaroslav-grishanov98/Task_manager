from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Класс для регистрации пользователя"""
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validated_email(self, value):  # Проверяет, что email уникален. Если такой email уже существует, выбрасывает ошибку.
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с такой почтой уже существует!')
        return value

    def create(self, validated_date):
        user = User.objects.create_user(
            username=validated_date['username'],
            email=validated_date['email'],
            password=validated_date['password']
        )
        return user


class EmailSerializer(AuthTokenSerializer):
    """Сериализатор для входа по почте и паролю"""
    email = serializers.EmailField(label='Email', write_only=True, help_text='Email адрес пользователя')
    username = None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()

            if user:
                attrs['user'] = authenticate(request=self.context.get('request'),
                                             username = user.username, password=password)
            else:
                attrs['user'] = None
            if not attrs['user']:
                msg = ('Невозможно войти с предоставленными данными')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Укажите email и пароль')
            raise serializers.ValidationError(msg, code='authorization')

        return attrs



