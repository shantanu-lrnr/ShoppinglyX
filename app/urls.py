from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
# from django.contrib.auth.urls
from django.conf import settings
from django.conf.urls.static import static
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('showcart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    # path('removecart/<int:id>/', views.remove_cart, name='removecart'),

    # path('add-to-cart/<int:id>/', views.add_to_cart, name='add-to-cart'),  #check krna hai.........................
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('buy/<int:pk>/', views.buy_now, name='buynow'),
    path('search/', views.search, name='search'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>/', views.laptop, name='laptopdata'),
    path('topwear/', views.top_wear, name='topwear'),
    path('topwear/<slug:data>/', views.top_wear, name='topweardata'),
    path('bottomwear/', views.bottom_wear, name='bottomwear'),
    path('bottomwear/<slug:data>/', views.bottom_wear, name='bottomweardata'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form = LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),

    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),

    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete",
        auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
        name="password_reset_complete",
    ),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
