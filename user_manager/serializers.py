from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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
        print("HERE")
        email = data.get("email")
        print("HERE2")
        pwd = data.get("password")
        if not email and not pwd:
            raise ValidationError("Both Email and Password are required.")

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise ValidationError("Account Does not Exists.")
        print(f"Data: {data}")
        return data

    def create(self, validated_data):
        user = authenticate(
            email=self.validated_data["email"], password=self.validated_data["password"]
        )
        print("FOUND user")
        if not user:
            raise ValidationError(
                {
                    "non_field_errors": ["Incorrect Password"],
                }
            )

        return Token.objects.get_or_create(user=user)[0]
