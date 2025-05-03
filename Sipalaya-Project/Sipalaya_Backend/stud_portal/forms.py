from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import StudentProfile, InstructorProfile, Assignment
from courses.models import CourseResource, Course

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'email', 'phone', 'address', 'gender']


class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = ['full_name', 'email', 'phone', 'address', 'gender']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'total_marks', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500', 'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'total_marks': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500', 'step': '0.01'}),
            'file': forms.FileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
        }
        labels = {
            'title': 'Assignment Title',
            'description': 'Description',
            'due_date': 'Due Date',
            'total_marks': 'Total Marks',
            'file': 'Assignment File',
        }
        help_texts = {
            'title': 'Enter a descriptive title for the assignment',
            'description': 'Provide detailed instructions for the assignment',
            'due_date': 'Select the due date and time',
            'total_marks': 'Enter the total marks for this assignment',
            'file': 'Upload the assignment file (PDF, DOC, etc.)',
        }

class GradeAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['marks_obtained', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }

class CourseResourceForm(forms.ModelForm):
    class Meta:
        model = CourseResource
        fields = ['title', 'description', 'file', 'resource_type', 'category', 'order', 'is_visible']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'resource_type': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'category': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'order': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
        }
        help_texts = {
            'title': 'Enter a descriptive title for the resource',
            'description': 'Provide a detailed description of the resource',
            'file': 'Upload the resource file',
            'resource_type': 'Select the type of resource',
            'category': 'Select the category of the resource',
            'order': 'Set the order of this resource in the course (lower numbers appear first)',
            'is_visible': 'Make this resource visible to students',
        }

class GradingRubricForm(forms.Form):
    criteria = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
        help_text='Enter the grading criteria (one per line)'
    )
    max_points = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
        help_text='Maximum points for this assignment'
    )

class BulkGradeForm(forms.Form):
    grades = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
        required=False,
        help_text='Common feedback for all selected submissions'
    )

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'image', 'skill_level', 'duration', 'price', 'syllabus', 'prerequisites']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'syllabus': forms.Textarea(attrs={'rows': 4}),
            'prerequisites': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'title': 'Enter a descriptive title for your course.',
            'description': 'Provide a detailed description of what students will learn.',
            'price': 'Enter the course price in NPR.',
            'duration': 'Enter the course duration in months.',
            'category': 'Select the most appropriate category for your course.',
            'image': 'Upload a course image (recommended size: 800x600px).',
            'is_active': 'Check this box to make the course visible to students.'
        }
