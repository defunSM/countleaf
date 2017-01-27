#!/usr/bin/env python
from django.shortcuts import render
from django.http import HttpResponse
from nltk import word_tokenize
from nltk import download
from collections import Counter
from textract import process
from time import time


from .models import Question, Choice
# Create your views here.

def letters(input):
    return ''.join(filter(str.isalpha, input))

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
        download("punkt")
        t0 = time()

        array = Counter(search_id.lower().split(" "))
        total = count_total(array)
        display = frequency_of_words(array, total)

        letter = len(letters(search_id))
        words = len(array)
        sentences = len(search_id.split("\n"))
        lettersperword = round(letter / words, 1)
        wordspersentence = round(words / sentences, 1)
        mostfrequentword = list(array.keys())[0]

        t1 = round(time() - t0, 3)
        context = {
            "words": words,
            "letters": letter,
            "sentences": sentences,
            "lettersperword": lettersperword,
            "wordspersentence": wordspersentence,
            "mostfrequentword": mostfrequentword,
            "time": t1,
            "method": "Text"

        }


        return render(request, 'wordapp/results.html', context)
        # return HttpResponse(str(array) + "<br/>Words: " + str(total) + "<br/><br/>" + display + "<br/>Time: " + str(t1) + "s")
    else:
        return render(request, 'wordapp/form.html')

def filesearch(request):
    if request.method == 'POST':
        download("punkt")

        if ".pdf" in str(request.FILES["myfile"]):
            text = request.FILES["myfile"].read()
            t0 = time()

            array = Counter(word_tokenize(str(text.lower())))
            total = count_total(array)
            display = frequency_of_words(array, total)

            letter = "N/A"
            words = "N/A"
            sentences = "N/A"
            lettersperword = "N/A"
            wordspersentence = "N/A"

        else:

            text = request.FILES["myfile"].read()
            t0 = time()

            array = Counter(word_tokenize(str(text.lower())))
            total = count_total(array)
            display = frequency_of_words(array, total)

            letter = len(letters(str(text)))
            words = len(text.decode().split(" "))
            sentences = len(text.decode().split("\n"))
            lettersperword = round(letter / words, 1)
            wordspersentence = round(words / sentences, 1)
            mostfrequentword = list(array.keys())[0]

        t1 = round(time() - t0, 3)
        context = {
            "words": words,
            "letters": letter,
            "sentences": sentences,
            "lettersperword": lettersperword,
            "wordspersentence": wordspersentence,
            "mostfrequentword": mostfrequentword,
            "time": t1,
            "method": "file " + "(" + str(request.FILES["myfile"]) + ")"
        }


        return render(request, 'wordapp/results.html', context)
