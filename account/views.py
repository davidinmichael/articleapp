from rest_framework import permissions
from django.contrib.auth.models import User

from blog import serializers
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken

# Register Class Based View
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if request.method == "POST":
            serializer = RegisterSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                user = serializer.save()
                # token = Token.objects.create(user=user).key
                refresh = RefreshToken.for_user(user)
                data['response'] = "Account created successfully"
                data['email'] = user.email
                data['username'] = user.username
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
            else:
                data = serializer.errors
            return Response(data)

# Register Function Based View
# @api_view(['POST',])
# @permission_classes([permissions.AllowAny])
# def register_view(request):
#     if request.method == 'POST':
#         serializer = RegisterSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             user = serializer.save()
#             token = Token.objects.create(user=user).key
#             data['respone'] = "Account Created Successfully"
#             data['email'] = user.email
#             data['username'] = user.username
#             data['token'] = token
        
    #     else:
    #         data = serializer.errors
    # return Response(data)

@api_view(['POST',])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"message": "You are logged out, Login to continue"})