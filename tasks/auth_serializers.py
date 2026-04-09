from rest_framework import serializers
from django.contrib.auth.models import User


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


