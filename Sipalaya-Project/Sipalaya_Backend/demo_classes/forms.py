from django import forms
from .models import DemoClass, DemoClassSchedule, DemoClassBooking, DemoClassFeedback
from django.utils import timezone
from datetime import datetime, timedelta

class DemoClassForm(forms.ModelForm):
    class Meta:
        model = DemoClass
        fields = ['course', 'title', 'description', 'instructor', 'max_participants']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class DemoClassScheduleForm(forms.ModelForm):
    class Meta:
        model = DemoClassSchedule
        fields = ['demo_class', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time < timezone.now():
                raise forms.ValidationError("Start time cannot be in the past.")
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time.")
            if (end_time - start_time) > timedelta(hours=2):
                raise forms.ValidationError("Demo class cannot be longer than 2 hours.")

class DemoClassBookingForm(forms.ModelForm):
    class Meta:
        model = DemoClassBooking
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available schedules
        self.fields['schedule'].queryset = DemoClassSchedule.objects.filter(
            is_booked=False,
            start_time__gt=timezone.now()
        )

class DemoClassFeedbackForm(forms.ModelForm):
    class Meta:
        model = DemoClassFeedback
        fields = ['rating', 'instructor_rating', 'content_rating', 'comment', 'would_recommend']
        widgets = {
            'rating': forms.RadioSelect(choices=DemoClassFeedback.RATING_CHOICES),
            'instructor_rating': forms.RadioSelect(choices=DemoClassFeedback.RATING_CHOICES),
            'content_rating': forms.RadioSelect(choices=DemoClassFeedback.RATING_CHOICES),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience...'}),
        } 