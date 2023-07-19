from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'},
                                             write_only=True, required=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        email = self.validated_data['email']
        username = self.validated_data['username']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password': "Passwords do not match"})
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': "User with that email already exists"})
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': "User with that username already exists"})
        elif len(password) < 5:
            raise serializers.ValidationError({"password": "Password must be longer than 5 characters"})
        else:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
            return user