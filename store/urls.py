from django.urls import path
from . import views
from .views import Login,signup,index,Logout,cart,checkout
from .views import order
from .middilewares.auth import auth_middleware
from .middilewares.auth1 import auth1_middleware
urlpatterns=[
    path('',index.as_view(),name="index"),
    path('signup',signup.as_view(),name="signup"),
    path('login',Login.as_view(),name="login"),
    path('logout',Logout.as_view(),name="logout"),
    path('cart', auth1_middleware(cart.as_view()),name="cart"),
    path('check-out',checkout.as_view(),name="checkout"),
    path('orders',auth_middleware(order.as_view()),name="orders"),
    path('otp',views.otp,name='otp')

]