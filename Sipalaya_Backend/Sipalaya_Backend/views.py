from django.shortcuts import redirect,render

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('homepage')  # Redirect if already logged in

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user automatically
            return redirect('homepage')
    else:
        form = UserCreationForm()
    
    return render(request, 'auth/signup.html', {'form': form})
