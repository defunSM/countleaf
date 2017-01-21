#!/usr/bin/env python
from django.shortcuts import render
from django.http import HttpResponse

from .models import Question, Choice
# Create your views here.

def index(request):
    context = {}
    return render(request, 'wordapp/index.html', context)
