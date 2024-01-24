from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from instamojo_wrapper import Instamojo
from django.conf import settings

api = Instamojo(api_key = settings.API_KEY, auth_token = settings.AUTH_TOKEN,
                endpoint='https://test.instamojo.com/api/1.1/')

def home(request):
    food = Food.objects.all()
    context = {'food' : food } 
    return render(request, 'home.html', context)

 
def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.warning(request, "Username Not Found.")
                return redirect('/login/')
            
            user_obj = authenticate(username = username, password = password)
            if user_obj:
                login(request, user_obj)
                return redirect('/')
            else:
                messages.warning(request, "Wrong Password")
            return redirect('/login/')

        except:
            messages.warning(request, "Somthing went wrong.")
            return redirect('/register/')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username = username)
            if user_obj.exists():
                messages.warning(request, "Username is already taken.")
                print(messages)
                return redirect('/register/')
            
            user_obj = User.objects.create(username = username)
            user_obj.set_password(password)
            user_obj.save()

            messages.success(request, "Account Created")
            print(messages)
            return redirect('/login/')
        
        except:
            messages.warning(request, "Something went wrong.")
            print(messages)
            return redirect('/login/')

    return render(request, 'register.html')


def add_to_cart(request, food_uid):
    user = request.user
    food_obj = Food.objects.get(uid = food_uid)
    cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_items = CartItems.objects.create(
        cart = cart,
        food = food_obj
    )
    return redirect('/')


def cart(request):
    cart = Cart.objects.get(user = request.user, is_paid = False)
    response = api.payment_request_create(
        amount = cart.order_total(),
        purpose = "Order",
        buyer_name = request.user.username,
        email = "gaurav714@gmail.com",
        redirect_url = "http://127.0.0.1:8000/success/"
    )
    context = {'cart' : cart, 'payment_url' : response['payment_request']['longurl']}
    return render(request, 'cart.html', context)


def remove_cart_item(request, cart_item_uid):
    try:
        CartItems.objects.get(uid = cart_item_uid).delete()
        return redirect('/cart/')
    except Exception as ex:
        print(ex)


def order(request):
    order = Cart.objects.filter(user = request.user, is_paid = True)
    context = {'order' : order}
    return render(request, 'order.html', context)

