from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone', 'address', 'profile_photo',
            'bio', 'date_of_birth', 'education', 'occupation',
            'linkedin_url', 'github_url', 'website_url'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        } 