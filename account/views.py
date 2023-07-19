from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

@api_view(['POST',])
@permission_classes([permissions.AllowAny])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user).key
            data['respone'] = "Account Created Successfully"
            data['email'] = user.email
            data['username'] = user.username
            data['token'] = token
        
        else:
            data = serializer.errors
    return Response(data)