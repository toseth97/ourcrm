from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.product, name="product"),
    path('create_customer/', views.create_customer, name="create_customer"),
    path('create_order/', views.create_order, name="create_order"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('delete_order/<str:pk>/', views.delete_order, name="delete_order"),
    path('update_customer/<str:pk>/',
         views.update_customer, name="update_customer"),
    path('delete_customer/<str:pk>/',
         views.delete_customer, name="delete_customer"),
    path('update_order/<str:pk>/',
         views.update_order, name="update_order"),
    path('place_order/<str:pk>/',
         views.place_order, name="place_order"),
    path("login/", views.loginPage, name="loginPage"),
    path("register/", views.registerPage, name="registerPage"),
    path("logout/", views.logoutUser, name="logout"),
    path("userpage/", views.userPage, name="userpage")
]
