from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from AuthApp.models import User


# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'role']

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return super().create(validated_data)


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'avatar', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
             email=validated_data['email'],
             username=validated_data.get('username', ''),
             phone_number=validated_data.get('phone_number', ''),
             avatar=validated_data.get('avatar', None),
             role=validated_data['role'],
             password=validated_data['password']
        )
        return user

