#!/usr/bin/env python
from django.shortcuts import render
from django.http import HttpResponse
from nltk import word_tokenize
from collections import Counter
from time import time


from .models import Question, Choice
# Create your views here.

def count_total(array):
    total = 0
    for key, value in array.items():
        total += value
    return total

def frequency_of_words(array, total):
    display = ""
    for key, value in array.items():
        display += str(key) + " - " + str(value) + " - " + str(float(value)/total) + "%" + "<br/>"
    return display

def index(request):
    context = {}
    return render(request, 'wordapp/index.html', context)

def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        t0 = time()

        array = Counter(word_tokenize(search_id.lower()))
        total = count_total(array)
        display = frequency_of_words(array, total)

        t1 = round(time() - t0, 3)
        return HttpResponse(str(array) + "<br/>Words: " + str(total) + "<br/><br/>" + display + "<br/>Time: " + str(t1) + "s")
    else:
        return render(request, 'wordapp/form.html')
