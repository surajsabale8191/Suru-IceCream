from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse, redirect,  get_object_or_404
from datetime import datetime
from Home.models import Contact, Product, Cart
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
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("registration")

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "registration.html")


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "login.html")

def products(request):
    products = Product.objects.all()

    return render(request, 'products.html', {
        'products': products
    })

@login_required(login_url='login')
def add_to_cart(request, icecream_id):

    product = get_object_or_404(Product, id=icecream_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.total_price for item in cart_items)

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })



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



def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.total_price for item in cart_items)

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total
    })       

@login_required
def payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)

    return render(request, "payment.html", {
        "total": total
    })