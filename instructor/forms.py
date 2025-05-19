from django import forms
from courses.models import Course, Lesson, Assignment
from .models import Resource, AssignmentFeedback, InstructorProfile
from django.utils.text import slugify

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'level', 'duration', 
                 'duration_weeks', 'price', 'enrollment_deadline', 'prerequisites', 
                 'image', 'is_featured', 'demo_class_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'prerequisites': forms.Textarea(attrs={'rows': 3}),
            'enrollment_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['module', 'title', 'content', 'video_url', 'order']
        widgets = {
            'module': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm'
            }),
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm',
                'placeholder': 'Enter lesson title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm',
                'rows': 6,
                'placeholder': 'Enter lesson content'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm',
                'placeholder': 'Enter video URL (optional)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm',
                'min': 1,
                'placeholder': 'Enter lesson order'
            })
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'resource_type', 'file', 'url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm',
                'placeholder': 'Enter resource title'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm',
                'placeholder': 'Enter resource description'
            }),
            'resource_type': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm'
            }),
            'file': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-primary-dark'
            }),
            'url': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm',
                'placeholder': 'Enter external URL if this is a link resource'
            })
        }
        help_texts = {
            'title': 'Enter a descriptive title for your resource',
            'description': 'Provide a brief description of the resource',
            'resource_type': 'Select the type of resource you are uploading',
            'file': 'Upload a file (PDF, DOC, DOCX, MP4, etc.)',
            'url': 'Enter an external URL if this is a link resource'
        }

    def clean(self):
        cleaned_data = super().clean()
        resource_type = cleaned_data.get('resource_type')
        file = cleaned_data.get('file')
        url = cleaned_data.get('url')

        if resource_type == 'link' and not url:
            raise forms.ValidationError('URL is required for link type resources')
        elif resource_type in ['video', 'document'] and not file:
            raise forms.ValidationError('File is required for video and document type resources')
        elif file and file.size > 10 * 1024 * 1024:  # 10MB limit
            raise forms.ValidationError('File size must be less than 10MB')

        return cleaned_data

class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        instructor = kwargs.pop('instructor', None)
        super().__init__(*args, **kwargs)
        if instructor:
            self.fields['lesson'].queryset = Lesson.objects.filter(
                module__course__instructor=instructor
            ).select_related('module', 'module__course')

    class Meta:
        model = Assignment
        fields = ['lesson', 'title', 'description', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = AssignmentFeedback
        fields = ['feedback', 'grade']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
            'grade': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.1}),
        }

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = ['bio', 'experience', 'certifications', 'profile_photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm'}),
            'experience': forms.Textarea(attrs={'rows': 4, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm'}),
            'certifications': forms.Textarea(attrs={'rows': 4, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm'}),
        } 