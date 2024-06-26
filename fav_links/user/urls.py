from django.urls import path, include
from user import views

urlpatterns = [
    path('register',views.Register.as_view()),
    path('login',views.Login.as_view()),
    path('refresh',views.Refresh.as_view()),
    path('logout',views.Logout.as_view()),
    path('resetpassword', views.ResetPassword.as_view()),
]