import os

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
from django.core.mail import send_mail

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import quote
from django.utils.html import strip_tags
User = get_user_model()

import os
from dotenv import load_dotenv
load_dotenv()

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
        token=default_token_generator.make_token(user)
        url_frontend = os.getenv('FRONTEND_URL')
        reset_link = f"{url_frontend}/reset-password/{uid}/{token}"

        html_message = f"""
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px;">
    <tr>
      <td align="center">

        <!-- Card -->
        <table width="100%" max-width="500px" cellpadding="0" cellspacing="0"
          style="background:#ffffff; border-radius:12px; padding:30px; box-shadow:0 4px 10px rgba(0,0,0,0.05);">

          <!-- Logo / App Name -->
          <tr>
            <td align="center">
            <img src="../media/Agromart_logo.png" alt="AgroMart Logo" width="80" style="margin-bottom:15px;">
              <h1 style="color:#4CAF50; margin-bottom:10px;">AgroMart</h1>
            </td>
          </tr>

          <!-- Title -->
          <tr>
            <td align="center">
              <h2 style="color:#333;">Reset Your Password</h2>
            </td>
          </tr>

          <!-- Message -->
          <tr>
            <td align="center">
              <p style="color:#555; font-size:14px; line-height:1.6;">
                We received a request to reset your password.
                Click the button below to set a new password.
              </p>
            </td>
          </tr>

          <!-- Button -->
          <tr>
            <td align="center">
              <a href="{reset_link}"
                 style="display:inline-block; margin-top:20px; padding:12px 25px;
                        background-color:#4CAF50; color:#ffffff;
                        text-decoration:none; border-radius:6px;
                        font-size:14px; font-weight:bold;">
                Reset Password
              </a>
            </td>
          </tr>

          <!-- Expiry -->
          <tr>
            <td align="center">
              <p style="margin-top:20px; font-size:12px; color:#888;">
                This link will expire in 1 hour.
              </p>
            </td>
          </tr>

          <!-- Fallback Link -->
          <tr>
            <td align="center">
              <p style="font-size:12px; color:#999;">
                If the button doesn’t work, copy and paste this link:
              </p>
              <p style="word-break:break-all; font-size:12px; color:#4CAF50;">
                {reset_link}
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center">
              <p style="margin-top:25px; font-size:11px; color:#aaa;">
                If you didn’t request this, you can safely ignore this email.
              </p>
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>
"""


        plain_message = strip_tags(html_message)
        try:
            send_mail(
                "Reset Your Password - AgroMart",
                plain_message,
                os.getenv('EMAIL_HOST_USER'),
                [email],
                html_message=html_message,
                fail_silently=False,
                )
        except Exception as e:

            print("EMAIL ERROR:", str(e))
            return Response({"error": "Email sending failed"}, status=500)
        
        return Response({"message": "Reset link sent to email"})

# rest pass
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response({"error": "Invalid link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Token expired"}, status=400)

        new_password = request.data.get("password")

        if not new_password:
            return Response({"error": "Password is required"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successful"})