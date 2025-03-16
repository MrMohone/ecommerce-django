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