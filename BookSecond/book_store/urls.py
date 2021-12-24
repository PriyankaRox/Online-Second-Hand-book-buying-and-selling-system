from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views
from .views import Login, Cart, Checkout,Cart1, Orders, SellView

urlpatterns = [
    url('^$', views.index, name='index1'),
    url('login', Login.as_view(), name='login'),
    url('logout', views.logout, name='logout'),
    url('signup', views.signup, name='signup'),
    url('shop', views.shop, name='shop'),
    #url('shop', Shop.as_view(), name='shop'),
    url('about', views.about, name='about'),
    url('view_p/(?P<my_id>\d+)/$', views.single, name='single_product'),
    url('cart', Cart.as_view(), name='cart'),
    url('checkout', Checkout.as_view(), name='checkout'),
    url('order', Orders.as_view(), name='orders'),
    url('sell', views.sell, name='sell'),
    #url('image' , views.Image , name='selling'),
    url('sview', SellView.as_view(), name="sell_view"),
    #url('pay',views.pay, name='payment'),
    #url('summary', views.summary,name = 'summary'),
    #url('cart/(?P<my_id>\d+)/$', Cart1.as_view(), name='remove'),
    url('success', views.success, name='success'),
    url('feedback', views.feedback, name='feedback'),
    url('forgot', views.forgot , name='forgot'),
    url('home',views.home,name='home'),


    path('reset_password',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name='password_reset'),
    path('reset_password_sent',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name='password_reset_complete')

]