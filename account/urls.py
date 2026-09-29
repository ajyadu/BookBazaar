from django.urls import path
from . import views as v

app_name="account"
urlpatterns = [
    path("signup/", v.signup, name="signup"),
    path("login/", v.login_view, name="login"),
    path("logout/", v.logout_view, name="logout"),
    path("profile/", v.profile, name="profile"),
    path("registerlistcreate",v.RegisterAPIView.as_view()),
    path("loginlistcreate",v.LoginAPIView.as_view()),
]