
from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.Register),
    path('login/',views.Login),
    path('profile/<int:user_id>/',views.Profile),
     path("forgot-password/",views.ForgotPasswordView.as_view()),
    path("reset-password/<uid>/<token>/", views.ResetPasswordView.as_view()),
]
