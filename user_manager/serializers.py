from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from user_manager.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True, source="key")
    email = serializers.EmailField(read_only=True, source="user.email")
    id = serializers.CharField(read_only=True, source="user.id")
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(read_only=True, source="user.name")
    is_superuser = serializers.BooleanField(read_only=True, source="user.is_superuser")

    class Meta:
        model = Token
        fields = (
            "token",
            "id",
            "email",
            "name",
            "password",
            "is_superuser",
        )

    def create(self, validated_data):
        pass

    def update(self, validated_data):
        pass


class LoginSerializer(UserSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = Token
        fields = (
            "token",
            "email",
            "id",
            "password",
            "name",
            "is_superuser",
        )

    def to_representation(self, obj):
        self.fields["email"] = serializers.EmailField(source="user.email")
        return super().to_representation(obj)

    def validate(self, data):
        email = data.get("email")
        pwd = data.get("password")
        if not email and not pwd:
            raise ValidationError("Both Email and Password are required.")

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise ValidationError("Account Does not Exists.")
        return data

    def create(self, validated_data):
        user = authenticate(
            email=validated_data["email"], password=validated_data["password"]
        )
        if not user:
            raise ValidationError(
                {
                    "non_field_errors": ["Incorrect Password"],
                }
            )

        return Token.objects.get_or_create(user=user)[0]


class RegisterUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=15, required=False)

    def validate(self, data):
        email = data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            return ValidationError(
                {"non_field_errors": ["This email is already in use."]}
            )
        if not data.get("password") == data.get("password2"):
            return ValidationError({"non_field_errors": ["Passwords do not match."]})

        del data["password2"]
        return data

    def create(self, validated_data):
        validated_data["is_active"] = True
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "last_login": {"read_only": True},
            "is_active": {"read_only": True},
        }
        exclude = (
            "is_superuser",
            "groups",
            "user_permissions",
            "is_staff",
            "last_login",
        )
