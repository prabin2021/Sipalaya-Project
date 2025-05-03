from django import forms
from .models import CourseResource, ResourceCategory

class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = CourseResource
        fields = ['title', 'description', 'file', 'resource_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'resource_type': forms.Select(choices=CourseResource.RESOURCE_TYPES),
        }

class ResourceCategoryForm(forms.ModelForm):
    class Meta:
        model = ResourceCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        } 