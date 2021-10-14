from Main.models import Book
from utils.books_prediction.NaiveBayesClassifier import NaiveBayesClassifier

from typing import Dict, List

from stop_words import get_stop_words
import pymorphy2
import json


def delete_chars(text: str) -> str:
    chars = ["«", "»", "…", "–", "(", ")", "[", "]", "#", ",", ".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ":", "+", "-", "/", "\\", "-", "!", "\"", "?"]

    for char in chars:
        text = str(text).replace(char, "")

    return text


def clean_texts(reviews: List) -> List:
    reviews_clear = []
    morph = pymorphy2.MorphAnalyzer()
    stop_words = get_stop_words('ru')

    for text in reviews:
        clear_text = ''

        text = delete_chars(text)

        for word in text.split():
            normal_form = morph.parse(word)[0].normal_form

            if not normal_form in stop_words:
                clear_text += normal_form + " "

        reviews_clear.append(clear_text)

    return reviews_clear


def get_prob_by_attr(clf: NaiveBayesClassifier, book: Book, attr: str) -> List:
    field_value = book[attr]
    X_train = clean_texts([field_value])

    return clf.predict(X_train, prob=True)


def sum_two_list(arr1: List, arr2: List) -> List:
    for ind, el in enumerate(arr2):
        arr1[ind] += el

    return arr1


def predict_book(path_to_clf: str, book: Book, prob=False) -> List:
    clf = NaiveBayesClassifier.load(path_to_clf)
    probabilities = [0 for i in range(len(clf.labels))]

    probability_name        = get_prob_by_attr(clf, book, "name")
    probability_description = get_prob_by_attr(clf, book, "description")

    probabilities = sum_two_list(probability_description, probability_name)

    label = clf.labels[probabilities.index(max(probabilities))]

    if prob:
        if label == "not_interested":
            return abs(probabilities.index(max(probabilities)))
        elif label == "":
            return 0

        return probabilities.index(max(probabilities))
    else:
        return label


def fit_by_response(clf: NaiveBayesClassifier, response: json) -> NaiveBayesClassifier:
    X_train = []
    y_train = []

    attrs = ["name", "description"]


    for book_id in response["categorizedBooks"]:
        book = Book.objects.get(id=book_id)

        for attr in attrs:
            X_train.append(getattr(book, attr))
            y_train.append(response["categorizedBooks"][X])

        X_train = clean_texts(X_train)

        clf.fit(X_train, y_train)

    return clf
