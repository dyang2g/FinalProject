from django.urls import path
from . import views

urlpatterns = [ #url paths
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('homepage', views.homepage, name="homepage"),
    path('plantinfo', views.plantinfo, name="plantinfo"),
    path('createplant', views.createplant, name="createplant"),
    path('error', views.error, name="error")
]