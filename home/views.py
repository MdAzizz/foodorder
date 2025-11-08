from django.shortcuts import render, redirect
from .models import User, ContactForm
from django.contrib import messages

# Create your views here.
def home(request):
    context = {'page' : 'Home'}
    return render(request, "index.html", context)

def menu(request):
    context = {'page' : 'Menu'}
    return render(request, "menu.html", context)

def about(request):
    context = {'page' : 'About'}
    return render(request, "about.html", context)

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        ContactForm.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been sent.")
        return redirect('/contact/')
        
    context = {'page' : 'Contact'}
    return render(request, "contact.html", context)

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        usr = User.objects.filter(email=email)
        if usr.exists():
            messages.error(request, "Email already registered.")
            return redirect('/register/')
        
        User.objects.create(name=name, email=email, password=password)
        messages.success(request, "Registration successful.")
        return redirect('/login/')
        
    context = {'page' : 'Register'}
    return render(request, "register.html", context)

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            usr = User.objects.get(email=email, password=password)
            messages.success(request, "Login successful.")
            request.session['user_name'] = usr.name
            return redirect('/')
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('/login/')
        
    context = {'page' : 'Login'}
    return render(request, "login.html", context)

def logout(request):
    try:
        del request.session['user_name']
    except KeyError:
        pass
    messages.success(request, "Logged out successfully.")
    return redirect('/login/')

def contactformView(request):
    contacts = ContactForm.objects.all().order_by('-created_at')
    context = {
        'page': 'Contact Form View',
        'contacts': contacts
    }
    return render(request, "contactformView.html", context)

def userformView(request):
    users = User.objects.all().order_by('-id')
    context = {
        'page': 'Registered Users',
        'users': users
    }
    return render(request, "userformView.html", context)