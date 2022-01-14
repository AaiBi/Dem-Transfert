from django.urls import path
from user import views


urlpatterns = [
    # Auth
    path('login/', views.login_user, name='login_user'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout_user'),
    path('password/', views.user_password_change, name='user_password_change'),
]