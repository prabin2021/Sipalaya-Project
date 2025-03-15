from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Banner, Feature
from courses.models import Course

def homepage_view(request):
    banners = Banner.objects.all()
    features =  Feature.objects.all()
    context = {
        'banners': banners,
        'features': features,
    }
    return render(request, 'base.html', context)

def about(request):
    return render(request, 'about.html')

def search_view(request):
    query = request.GET.get('q', '').strip()
    courses = Course.objects.filter(title__icontains=query) if query else []
    return render(request, 'homepage/search.html', {'courses': courses, 'query': query})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('protected_page.html')  # Redirect logged-in users

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('protected_page')  # Redirect after successful login
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('protected_page.html')  # Redirect if already logged in

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('protected_page.html')
    else:
        form = UserCreationForm()

    return render(request, 'auth/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('base.html')

@login_required(login_url='/auth/login/')
def protected_page(request):
    banners = Banner.objects.all()
    features = Feature.objects.all()
    context = {
        'banners': banners,
        'features': features,
    }
    return render(request, 'protected_page.html', context)