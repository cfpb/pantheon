from django.http import HttpResponse

# Create your views here.

def release_existing(request):
    return HttpResponse('release existing repo')

def start_new(request):
    return HttpResponse('start new repo')
