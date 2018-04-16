from django.urls import path
from . import views

app_name = "rrsite"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login),
    path('register', views.register_view),

    path('register/email', views.register_email),
    path('register/phone', views.register_phone),

    path('forgetpassword', views.forgetpassword),

    path('api/recommend/category', views.recommend_restaurant),
]
