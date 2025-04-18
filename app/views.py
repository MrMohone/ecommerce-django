from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View

from app import admin
from .models import Cart, Product,Customer
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q #Q is required for multiple conditions
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@login_required#ALL FUNCTIONS ARE WORK ONLY IF USER IS LOGIN
def home(request):
    return render(request, "app/home.html")

@login_required
def about(request):
    return render(request, "app/about.html")

@login_required
def contact(request):
    return render(request, "app/contact.html")

@method_decorator(login_required, name='dispatch')#ALL CLASS ARE WORK ONLY IF USER IS LOGIN
class CategoryView(View):
    def get(self, request, val):
        #Fetch from db
        product = Product.objects.filter(category=val)#fetch all matched values like title, price...
        title = Product.objects.filter(category=val).values('title')#fetch only title
        return render(request, 'app/category.html', locals())

@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', locals())


@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', locals())
        
#@method_decorator(login_required, name='dispatch') :#🙌WEDN'T NEED FOR REGISTRATION 
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

        
@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
def address(request):
    add = Customer.objects.filter(user=request.user)#login user
    return render(request, 'app/address.html', locals())

@method_decorator(login_required, name='dispatch')
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
    

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required    
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value 
    totalamount = amount + 40 #40 for shipping price
        
    return render(request, 'app/addtocart.html', locals())


@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self,request):
        user = request.user#login user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        # razoramount = int( totalamount * 100)
        # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        # data = {'amount': razoramount, 'currency': 'INR', 'receipt': 'order_rcptid_12'}
        # payment_response = client.order.create(data=data)
        # print(payment_response)
        return render(request, 'app/checkout.html',locals())
    
    
#linked from myscript.js
@login_required
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

@login_required      
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


@login_required
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

        
@login_required
def search(request):
    query = request.GET.get('search')
    totalitem = 0
    # wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        # wishitem = len(wishitem.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query) )#name
    return render(request, 'app/search.html', locals())


