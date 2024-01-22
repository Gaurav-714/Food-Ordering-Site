from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate

def home(request):
    food = Food.objects.all()
    context = {'food' : food } 
    return render(request, 'home.html', context)

 
def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects,filter(username = username)
            if not user_obj.exists():
                messages.error(request, "Username Not Found.")
                return redirect('/login/')
            
            user_obj = authenticate(username = username, password = password)
            if user_obj:
                login(request, user_obj)
                return redirect('/')
            messages.error(request, "Wrong Password")

        except Exception as ex:
            return


    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username = username)
            if user_obj.exists():
                messages.error(request, "Username is already taken.")
                return redirect('/register/')
            
            user_obj = User.objects.create(username = username)
            user_obj.set_password(password)
            user_obj.save()

            messages.success(request, "Account Created")
            return redirect('/login/')
        
        except Exception as ex:
            messages.error(request, "Something went wrong.")
            return redirect('/login/')

    return render(request, 'register.html')



def add_to_cart(request):
    return redirect('/')