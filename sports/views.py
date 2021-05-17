from django.shortcuts import render


# Create your views here.
def sports_index(request):
    return render(request, 'sports/index.html')
