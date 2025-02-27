from django.shortcuts import redirect,render

def basehome(request):
    return render(request,'homepage.html')