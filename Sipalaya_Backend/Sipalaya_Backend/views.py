from django.shortcuts import redirect,render
from homepage.views import homepage_view
from homepage.models import Banner,Feature
# def basehome(request):
#     return render(request,'homepage.html')

def homepage_view(request):
    banners = Banner.objects.all()
    features =  Feature.objects.all()
    context = {
        'banners': banners,
        'features': features,
    }
    return render(request, 'homepage.html', context)