from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from AuthApp.models import User
from .serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# -----------------------
# Register
# -----------------------
from rest_framework.parsers import MultiPartParser, FormParser
# @parser_classes([MultiPartParser, FormParser])
@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "User registered successfully",
            "id": user.id,
            "role": user.role
        }, status=201)
    return Response(serializer.errors, status=400)

# -----------------------
# Login (JWT)
# -----------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=400)

    user = authenticate(request, email=email, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)

    # Generate JWT token
    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        },
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })

# -----------------------
# Profile (JWT protected)
# -----------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Profile(request, user_id):
    if request.user.id != user_id:
        return Response({"error": "Unauthorized"}, status=403)

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


#! ================================
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
User = get_user_model()
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}/"

        send_mail(
            "Password Reset",
            f"Click here to reset password: {reset_link}",
            "your@email.com",
            [email],
            fail_silently=False,
        )

        return Response({"message": "Reset link sent to email"})

# reset password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except:
            return Response({"error": "Invalid link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Token expired"}, status=400)

        new_password = request.data.get("password")
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successful"})