from django.shortcuts import render,HttpResponse, redirect,  get_object_or_404
from datetime import datetime
from Home.models import Contact, Registration, Product, Cart
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index (request):
    context ={
        "variable":"This is sent"
    }
    return render(request, "index.html", context)
    #return HttpResponse("This is home page")

def about(request):
    return render(request, "about.html")
    #return HttpResponse("This is about page")

def services(request):
    return render(request, "services.html")
    #return HttpResponse(" THis is services page")

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact=Contact(name=name, email=email, phone=phone,desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, "Your message has been sent.")

    return render(request, "contact.html")
    #return HttpResponse(" THis is contact page")

def registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        registration=Registration(name=name, email=email, password=password, date=datetime.today())
        registration.save()
        messages.success(request, "Registration Successfull")

    return render(request, "registration.html")



def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = Registration.objects.get(
                email=email,
                password=password
            )

            request.session["user_id"] = user.id
            return redirect("home")

        except Registration.DoesNotExist:
            return render(request, "login.html", {
                "error": "Invalid email or password"
            })

    return render(request, "login.html")

def products(request):
    products = Product.objects.all()

    return render(request, 'products.html', {
        'products': products
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('products')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.total_price for item in cart_items)

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required
def decrease_quantity(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart')

        