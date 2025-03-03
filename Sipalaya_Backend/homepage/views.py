from django.shortcuts import render
from .models import Banner, Feature
from courses.models import Course

def homepage_view(request):
    banners = Banner.objects.all()
    features =  Feature.objects.all()
    print("HI HI")
    print("Banners QuerySet:", banners)  # Debugging
    context = {
        'banners': banners,
        'features': features,
    }
    return render(request, 'homepage.html', context)


def search_view(request):
    query = request.GET.get('q', '').strip()
    courses = Course.objects.filter(title__icontains=query) if query else []
    return render(request, 'homepage/search.html', {'courses': courses, 'query': query})
