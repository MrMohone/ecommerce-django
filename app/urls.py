from django.urls import path

from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordRestForm, MyPasswordChangeForm,MySetPasswordForm
from . import views

urlpatterns = [
    path("", views.home ),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path("category/<slug:val>", views.CategoryView.as_view(), name='category'),#as.view() => for class
    path("category-title/<val>", views.CategoryTitle.as_view(), name="product-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name='product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    
    path('search/', views.search, name='search'),
    
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),
   
    
    #registration authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistartion'),
    #for login no need class/fun in views.py
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',
    authentication_form=LoginForm), name='login'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
     #password done message displayer
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    
    #reset password
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',
                form_class=MyPasswordRestForm), name='password-reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    
    path('password-reset-confrim/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confrim.html',form_class=MySetPasswordForm),name='password_reset_confrim'),
    
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#for displaying images

admin.site.site_header = "Neel Dairy"
admin.site.site_title = "Neel Dairy"
admin.site.site_index_title = "Welcome to Neel Shop"