from django.urls import path

from .views import SignUp, Login, UserInfo

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("user-info/", UserInfo.as_view(), name="user_info"),
]