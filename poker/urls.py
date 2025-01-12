from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register

urlpatterns = [
    path('upload/', views.upload_bot, name='upload_bot'),
    # path('run_match/<int:bot1_id>/<int:bot2_id>/', views.run_match, name='run_match'),
    path('auth/register/', register, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('',views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('bots/', views.bots, name='bots'),
    path('replay/<int:game_id>/', views.replay, name='replay'),
]
