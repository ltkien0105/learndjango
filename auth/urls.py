from django.urls import path

from .views import SignUp, Login, UserInfo, Logout, CookieTokenRefreshView

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("user-info/", UserInfo.as_view(), name="user_info"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="token-refresh"),
]