from django import forms
from .models import Course, Module, Lesson, Assignment, Review
from feedback.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'content': forms.Textarea(attrs={'rows': 6}),
        } 