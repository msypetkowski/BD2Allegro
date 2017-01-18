from django.shortcuts import render
from django.http import HttpResponse


def notLoggedClient(request):
    return HttpResponse("Internet shop home page (TODO)")
