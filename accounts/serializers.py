from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone', 'account_number', 'bank_name', 'account_name')
        extra_kwargs = {
            'email': {'required': False},
            'bank_name': {'required': False},
            'account_number': {'required': False},
            'account_name': {'required': False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        user.phone = validated_data.get('phone', '')
        user.bank_name = validated_data.get('bank_name', '')
        user.account_number = validated_data.get('account_number', '')
        user.account_name = validated_data.get('account_name', '')
        user.save()
        return user