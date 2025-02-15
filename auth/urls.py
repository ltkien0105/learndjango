from django.urls import path

from .views import SignUp, Login, UserInfo, Logout, SetCsrfToken

urlpatterns = [
    path("set-csrf-token/", SetCsrfToken.as_view(), name="set-csrf-token"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("user/", UserInfo.as_view(), name="user_info"),
    path("signup/", SignUp.as_view(), name="signup"),
    # path("refresh/", CookieTokenRefreshView.as_view(), name="token-refresh"),
]