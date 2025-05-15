from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm

# Create your views here.

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile_update')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/profile_update.html', {
        'form': form,
        'user': request.user
    })
