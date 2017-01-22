#!/usr/bin/env python
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        return HttpResponse(str(search_id))
    else:
        return render(request, 'countleaf/index.html')


def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        return HttpResponse(str(search_id))
    else:
        return render(request, 'wordapp/form.html')
