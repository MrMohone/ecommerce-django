from django.shortcuts import render
from django.db.models import Count
from django.views import View
from .models import Product

def home(request):
    return render(request, "app/home.html")

class CategoryView(View):
    def get(self, request, val):
        #Fetch from db
        product = Product.objects.filter(category=val)#fetch all matched values like title, price...
        title = Product.objects.filter(category=val).values('title')#fetch only title
        return render(request, 'app/category.html', locals())

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', locals())



class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', locals())