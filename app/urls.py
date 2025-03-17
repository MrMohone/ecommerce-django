from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordRestForm
from . import views

urlpatterns = [
    path("", views.home ),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path("category/<slug:val>", views.CategoryView.as_view(), name='category'),#as.view() => for class
    path("category-title/<val>", views.CategoryTitle.as_view(), name="product-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name='product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.ProfileView.as_view(), name='address'),
    
    
    #registration authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistartion'),
    #for login no need class/fun in views.py
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',
    authentication_form=LoginForm), name='login'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',
                                            form_class=MyPasswordRestForm), name='password-reset'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#for displaying images
