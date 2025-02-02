from django.shortcuts import render
from django.http import HttpResponse

def aboutPage(request):
    return HttpResponse('hi')