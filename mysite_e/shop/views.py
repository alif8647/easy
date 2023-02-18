from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Cart, Customer, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    totalitem = 0
    topwears = Product.objects.filter(category='TW')
    bottomwears = Product.objects.filter(category='BW')
    mobails = Product.objects.filter(category='S')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'shop/home.html',
                  {'topwears': topwears, 'bottomwears': bottomwears, 'mobails': mobails, 'totalitem': totalitem})


def shoes(request, data=None):
    if data is None:
        shoes = Product.objects.filter(category='S')
    elif data == 'low':
        shoes = Product.objects.filter(category='S').filter(discounted_price__lte=1500)
    elif data == 'high':
        shoes = Product.objects.filter(category='S').filter(discounted_price__gt=1500)
    return render(request, 'shop/shoes.html', {'shoes': shoes})


def tobwear(request, data=None):
    if data is None:
        top = Product.objects.filter(category='TW')
    elif data == 'low':
        top = Product.objects.filter(category='TW').filter(discounted_price__lte=2000)
    elif data == 'high':
        top = Product.objects.filter(category='TW').filter(discounted_price__gt=2000)
    return render(request, 'shop/top.html', {'top': top})


def bottomwear(request, data=None):
    if data is None:
        bottom = Product.objects.filter(category='BW')
    elif data == 'low':
        bottom = Product.objects.filter(category='BW').filter(discounted_price__lte=1300)
    elif data == 'high':
        bottom = Product.objects.filter(category='BW').filter(discounted_price__gt=1300)
    return render(request, 'shop/bottom.html', {'bottom': bottom})


def product_detail(request, pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'shop/productdetail.html',
                  {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})


@login_required()
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required()
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        totalitem = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for cat in cart_product:
                temtamount = (cat.quantity * cat.product.discounted_price)
                amount += temtamount
                totalamount = amount + shipping
            return render(request, 'shop/addtocart.html',
                          {'carts': cart, 'amount': amount, 'totalamount': totalamount, 'totalitem': totalitem})
        else:
            return render(request, 'shop/emptycart.html', {'totalitem': totalitem})


@login_required()
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for cat in cart_product:
            temtamount = (cat.quantity * cat.product.discounted_price)
            amount += temtamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping
        }

        return JsonResponse(data)


@login_required()
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for cat in cart_product:
            temtamount = (cat.quantity * cat.product.discounted_price)
            amount += temtamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping
        }

        return JsonResponse(data)


@login_required()
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for cat in cart_product:
            temtamount = (cat.quantity * cat.product.discounted_price)
            amount += temtamount

        data = {
            'amount': amount,
            'totalamount': amount + shipping,

        }

        return JsonResponse(data)


@login_required()
def profile(request):
    totalitem = 0
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            road = form.cleaned_data['road']
            postcode = form.cleaned_data['postcode']
            thana = form.cleaned_data['thana']
            district = form.cleaned_data['district']
            reg = Customer(user=usr, name=name, road=road, postcode=postcode, thana=thana, district=district)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Update Successfully ')
        return render(request, 'shop/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})
    else:
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'shop/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})


@login_required()
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'shop/address.html', {'add': add, 'active': 'btn-primary', 'totalitem': totalitem})


@login_required()
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'shop/orders.html', {'oreder': op})



class CheckoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_item = Cart.objects.filter(user=user)
        amount = 0.0
        shipping = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for cat in cart_product:
                temtamount = (cat.quantity * cat.product.discounted_price)
                amount += temtamount
            totalamount = amount + shipping
        return render(request, 'shop/checkout.html',
                      {'add': add, 'totalamount': totalamount, 'cart_item': cart_item, 'totalitem': totalitem})



class PaymentdonetView(View):
    def get(self, request):
        user = request.user
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
            c.delete()
        return redirect('orders')


@login_required()
def change_password(request):
    return render(request, 'shop/changepassword.html')


@login_required()
def mobile(request):
    return render(request, 'app/mobile.html')


'''class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'shop/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registration Successfully ')
            form.save()
        return render(request, 'shop/customerregistration.html', {'form': form})'''
def customerregistation(request):
    if request.method =='POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registration Successfully ')
            form.save()
        return render(request, 'shop/customerregistration.html', {'form': form})
    else:
        form = CustomerRegistrationForm()
        return render(request, 'shop/customerregistration.html', {'form': form})


def search(request):
    if request.method == 'GET':
        query = request.GET.get('quary')
        if query:
            product = Product.objects.filter(title__icontains=query)
            return render(request, 'shop/search.html', {'product': product})
        else:
            print('This product is not available')
            return render(request, 'shop/search.html')
