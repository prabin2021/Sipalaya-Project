from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'email', 'phone', 'address', 'gender']
        widgets = {
            'gender': forms.Select(choices=StudentProfile.GENDER_CHOICES),
        }
