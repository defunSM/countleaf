#!/usr/bin/env python
import requests as req
import enchant

from django.shortcuts import render
from django.http import HttpResponse
from nltk import word_tokenize, sent_tokenize
from nltk import download
from collections import Counter
from textract import process
from time import time
from bs4 import BeautifulSoup

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

def urlsearch(request):
    search_id = request.POST.get('url', None)

    t0 = time()
    resp = req.get(str(search_id))
    soup = BeautifulSoup(resp.text, 'lxml')
    array = []
    wordarray = []
    letters = 0
    d = enchant.request_pwl_dict("usa.txt")

    # Array does not exclude the tags

    for h in soup.find_all('p'):
        array.append(word_tokenize(str(h)))


    sentences = len(array)

    for x in array:
        for i in x:
            if d.check(i.lower()):
                count = len(i)
                if count != 1 or i == 'i' or i == 'I' or i == 'A' or i == 'a':
                    wordarray.append(i.lower())
                    letters += len(i)


    words = len(wordarray)

    mostfrequentword = list(Counter(wordarray).keys())[0]


    t1 = round(time() - t0, 3)
    context = {
        "words": words,
        "letters": letters,
        "sentences": sentences,
        "lettersperword": round(letters/words, 1),
        "wordspersentence": round(words/sentences, 1),
        "mostfrequentword": mostfrequentword,
        "time": t1,
        "method": "Url " + "(" + str(search_id) + ")",
    }
    return render(request, 'wordapp/results.html', context)
