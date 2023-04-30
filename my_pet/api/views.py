from django.http import HttpResponse

def index(request):
    return HttpResponse('This my "Pet project"')