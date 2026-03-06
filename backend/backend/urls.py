
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include("AuthApp.urls")),
    path("api/contactapp/", include("ContactApp.urls")),
    path("api/farmer/",include("FarmerApp.urls")),


     path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




