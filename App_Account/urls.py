from django.urls import path
app_name = 'App_Account'
from .import views
urlpatterns = [
    path('signup/',views.SignupView,name="signup"),
    path('login/',views.LoginpView,name="login"),
    path('logout/',views.Logout_view,name="logout"),
    path('dashboard/',views.DashBoard,name="dashboard"),
    path('update/',views.UpdateProfile,name="update"),
]
