from django.http import HttpResponse

# Create your views here.
def initialize_ci(request):
    return HttpResponse('initialize CI job')