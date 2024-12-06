from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit_profile/', views.user_profile_update, name='profile_update'),
    path('profile/edit_profile/resetPassword/', views.password_change, name='resetPassword')
]