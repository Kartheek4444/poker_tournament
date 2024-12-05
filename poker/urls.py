from django.urls import path
from .views import upload_bot, run_match, leaderboard
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register

urlpatterns = [
    path('upload/', upload_bot, name='upload_bot'),
    path('run_match/<int:bot1_id>/<int:bot2_id>/', run_match, name='run_match'),
    path('auth/register/', register, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]
