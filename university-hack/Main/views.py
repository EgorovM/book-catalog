import json
import random
import glob
from typing import Dict, List

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from Main.models import Book

from utils.books_prediction.NaiveBayesClassifier import NaiveBayesClassifier
from utils.books_prediction.clf_helper import predict_book, fit_by_response


@require_GET
def index(request):
    # TODO: нормально реализовать уникальные имена классификаторов.json,
    # Пытался через кол-во файлов в каталоге, НЕ ПОЛУЧИЛОСЬ ;(

    number_of_classificators = len(glob.glob('/classificators/')) + 1
    path_to_user_classificator = f"classificators/{number_of_classificators}.json"

    if not 'categories' in request.session:
        request.session['categories'] = {}
        # request.session['path_to_clf'] = path_to_user_classificator
        # NaiveBayesClassifier().save(path_to_user_classificator)
        # For test you can change "path_to_clf" session to "classificators/test.json"
        # and comment two top codes
        request.session['path_to_clf'] = "classificators/test.json"

    return render(request, 'index.html')


@csrf_exempt
@require_POST
def categories(request):
    data = request.body
    json_data = json.loads(data)

    current_categories = request.session['categories']
    current_categories.update(json_data)

    path_to_clf = request.session['path_to_clf']

    new_books = find_new_books(current_categories, path_to_clf)
    return JsonResponse({'books': new_books}, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_POST
def train_clf(request):
    path_to_clf = request.session['path_to_clf']
    # TODO: add name %NAME_OF_CATEGORIZED_BOOKS%
    categorized_books = json.dumps(request.POST['NAME_OF_CATEGORIZED_BOOKS'])
    clf = NaiveBayesClassifier.load(path_to_clf)
    clf = fit_by_response(clf, categorized_books)
    clf.save(path_to_clf)
    return JsonResponse({'error': None}, json_dumps_params={'ensure_ascii': False})


def find_new_books(categories: Dict[int, str], path_to_clf: str) -> List[Dict]:
    books = get_random_books(12)
    books = classify_books(books, path_to_clf, sort=True)

    return books


def get_random_books(num: int):
    books = Book.objects.all().values()
    books = [book for book in books]
    random_books = random.sample(books, 12)
    return random_books


def classify_books(books: List, path_to_clf: str, sort=False) -> List:
    clf = NaiveBayesClassifier.load(path_to_clf)

    for ind, book in enumerate(books):
        book["category"] = predict_book(path_to_clf, book) if len(clf.dictionary) != 0 else ""
        books[ind] = book

    if sort:
        print('sorting...')
        books.sort(key=lambda book: predict_book(path_to_clf, book, prob=True))

    return books
