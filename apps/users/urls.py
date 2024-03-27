from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

from apps.users import views

router = DefaultRouter()
router.register('', views.UserAPIView, "api_users")

urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='api_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_refresh'),
]

urlpatterns += router.urls