from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

def landing(request):
    return render(
        request,
        'single_pages/index.html',
    )


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )