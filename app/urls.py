from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.home ),
    path("category/<slug:val>", views.CategoryView.as_view(), name='category'),
    path("category-title/<val>", views.CategoryTitle.as_view(), name="product-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name='product-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#for displaying images
