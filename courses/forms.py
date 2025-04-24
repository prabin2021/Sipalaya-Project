from django import forms
from .models import Course, Module, Lesson, Review

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'description', 'thumbnail', 'price', 'duration', 'level', 'prerequisites', 'what_you_will_learn', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'prerequisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'what_you_will_learn': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tags separated by commas'}),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'duration', 'order']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter video URL'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}, choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Share your experience with this course'}),
        } 