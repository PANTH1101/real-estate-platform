from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User, UserRole


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "password", "full_name", "phone_number", "role")

    def validate_role(self, value: str):
        if value not in (UserRole.BUYER, UserRole.SELLER):
            raise serializers.ValidationError("role must be BUYER or SELLER")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            email=attrs.get("email"),
            password=attrs.get("password"),
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name", "phone_number", "role", "is_email_verified", "created_at", "updated_at")
        read_only_fields = ("id", "email", "role", "is_email_verified", "created_at", "updated_at")


