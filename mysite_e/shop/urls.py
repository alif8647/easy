from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('', views.home, name='home'),
                  path('shoes/', views.shoes, name='shoes'),
                  path('shoes/<slug:data>', views.shoes, name='shoesdata'),
                  path('top/', views.tobwear, name='top'),
                  path('top/<slug:data>', views.tobwear, name='topdata'),
                  path('bottom/', views.bottomwear, name='bottom'),
                  path('bottom/<slug:data>', views.bottomwear, name='bottomdata'),
                  path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
                  path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
                  path('cart/', views.show_cart, name='showcart'),
                  path('pluscart/', views.plus_cart),
                  path('minuscart/', views.minus_cart),
                  path('removecart/', views.remove_cart),
                  path('accounts/login/',
                       auth_views.LoginView.as_view(template_name='shop/login.html', authentication_form=LoginForm),
                       name='login'),
                  #path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
                  path('registration/', views.customerregistation, name='customerregistration'),
                  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
                  path('profile/', views.profile, name='profile'),
                  path('address/', views.address, name='address'),
                  path('orders/', views.orders, name='orders'),
                  path('passwordchange/', auth_views.PasswordChangeView.as_view(
                      template_name='shop/passwordchange.html', form_class=MyPasswordChangeForm,
                      success_url='/passwordchangedone/'), name='passwordchange'),
                  path('passwordchangedone/',
                       auth_views.PasswordChangeView.as_view(template_name='shop/passwordchangedone.html'),
                       name='passwordchangedone'),
                  path('mobile/', views.mobile, name='mobile'),
                  path('search/', views.search, name='search'),
                  path('checkout/', views.CheckoutView.as_view(), name='checkout'),
                  path('paymentdone/', views.PaymentdonetView.as_view(), name='paymentdone'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
