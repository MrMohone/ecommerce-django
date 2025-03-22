from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.db.models import Count
from django.views import View
from .models import Cart, Product,Customer
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q #Q is required for multiple conditions


def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

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

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    
    def post(self, request):# when we submit form, come here
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
            
        return render(request, 'app/customerregistration.html', locals())

class ProfileView(View):
     def get(self, request):
        form = CustomerProfileForm
        return render(request, 'app/profile.html', locals())

     def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
           user = request.user
           name = form.cleaned_data['name']
           locality = form.cleaned_data['locality']
           city = form.cleaned_data['city']
           mobile = form.cleaned_data['mobile']
           state = form.cleaned_data['state']
           zipcode = form.cleaned_data['zipcode']
            #insert to custemer table
           reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
           reg.save()
           messages.success(request, "Congratulations! Profile Save Successfully")
        else:
           messages.warning(request, "Invalid Input Data")

        return render(request, 'app/profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)#login user
    return render(request, 'app/address.html', locals())


class updateAddress(View):
    def get(self,request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)#omg
        return render(request, 'app/updateAddress.html', locals())
    
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
             add = Customer.objects.get(pk=pk)
             add.name = form.cleaned_data['name']
             add.locality = form.cleaned_data['locality']
             add.city = form.cleaned_data['city']
             add.mobile = form.cleaned_data['mobile']
             add.state = form.cleaned_data['state']
             add.zipcode = form.cleaned_data['zipcode']
             add.save()
             messages.success(request, "Congratulations! Profile Update Successfully")
        else:
             messages.warning(request,'Invalid Input Data')
        return redirect('address')
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    
    Cart(user=user, product=product).save()
    return redirect('/cart')
    
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value 
    totalamount = amount + 40 #40 for shipping price
        
    return render(request, 'app/addtocart.html', locals())

#linked from myscript.js
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        # Q is required for multiple conditions
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        if c:
            c.quantity += 1  # current quantity increase by one
            c.save()  # update the cart

            # now, get data from cart
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = amount + 40

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
        
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        # Q is required for multiple conditions
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        if c:
            c.quantity -= 1  # current quantity increase by one
            c.save()  # update the cart

            # now, get data from cart
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = amount + 40

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart item not found'}, status=404)



def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)