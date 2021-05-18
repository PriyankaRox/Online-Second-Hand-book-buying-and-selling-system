from django.contrib import admin
from django.urls import path
from .middlewares.auth import auth_middleware
from .views import Index, Signup, Login, logout, Cart, CheckOut, OrderView

from .views import index1, shop1, about, singleproduct, Cart1, CheckOut1, OrderView1, payment,  mail

app_name = 'book_store'

urlpatterns = [
    path('', index1.as_view(), name='home'),
    #path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', Cart.as_view(), name='cart'),
    path('check-out', CheckOut.as_view(), name='check-out'),
    path('order', auth_middleware(OrderView.as_view()), name='order'),
    path('shop', shop1.as_view(), name='shop'),
    path('cart1', Cart1.as_view(), name='cart1'),
    path('checkout', CheckOut1.as_view(), name='checkout'),
    path('order1', OrderView1.as_view(), name='order'),
    path('payment', payment, name='payment'),
    path('singleproduct', singleproduct),
    path('about', about),
    #path('success' , success , name='success'),
    path('mail', mail),
    #path('', index1.as_view(), name='home'),
]
