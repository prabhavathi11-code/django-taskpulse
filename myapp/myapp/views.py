from django.http import HttpResponse

def greet(request):
    return HttpResponse("Hello Prabhavathi! Welcome to Django!")