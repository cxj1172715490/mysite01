from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index_view(request):
    # return HttpResponse('这是新闻频道的首页')
    return render(request, 'index.html')