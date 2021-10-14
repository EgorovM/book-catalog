import pymorphy2
import math
import json


class NaiveBayesClassifier:

    """
        docs

        clf.fit(X_train, y_train) X_train - названия книг, y_train - 1, если лайк, 0, если не лайк
        clf.preict(X) - возвращает список предсказанных меток

        >>> clf.fit(["я выйду убивац", "никогда не надо умирац"], [1, 0])
        >>> clf.predict(["никогда не выйду", "я убивац"])
        [0, 1]

        method predict()
        attr prob: return probabilities in ln
    """

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.morph = pymorphy2.MorphAnalyzer()
        self.dictionary = {}
        self.labels = ["interested", "not_interested", ""]
        self.labels_count = dict.fromkeys(self.labels, 0)
        self.size = 0
        self.word_probability = {}

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """

        for ind, text in enumerate(X):
            for word in text.split():
                norm_form = self.morph.parse(word)[0].normal_form

                if not norm_form in self.dictionary:
                    self.dictionary[norm_form] = dict.fromkeys(self.labels, 0)
                    self.size += 1

                if not norm_form in self.word_probability:
                    self.word_probability[norm_form] = dict.fromkeys(self.labels, 0)

                self.dictionary[norm_form][y[ind]] += 1

            self.labels_count[y[ind]] += 1

        for word in self.dictionary:
            for label in self.labels_count.keys():
                nc  = sum([self.dictionary[w][label] for w in self.dictionary])
                nic = self.dictionary[word][label]
                self.word_probability[word][label] = (nic + self.alpha) / (nc + self.size * self.alpha)

    def predict(self, X, prob=False):
        """ Perform classification on an array of test vectors X. """
        results = []

        for ind, text in enumerate(X):
            probabilities = dict.fromkeys(self.labels, 0)

            for label in probabilities:
                prob = self.labels_count[label] / sum(self.labels_count.values()) if sum(self.labels_count.values()) != 0 else 0
                probabilities[label] = math.log(prob) if prob != 0 else -100000

            for word in text.split():
                norm_form = self.morph.parse(word)[0].normal_form

                for label in self.labels:
                    if norm_form in self.word_probability:
                        probabilities[label] += math.log(self.word_probability[norm_form][label])

            max_prob = max(probabilities.values())

            for label in probabilities:
                if probabilities[label] == max_prob:
                    results.append(label)
                    break

        if prob:
            return list(probabilities.values())
        else:
            return results

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        y_pred = self.predict(X_test)

        results = [1 if y_pred[i] == y_test[i] else 0 for i in range(len(y_test))]

        return sum(results) / len(results)

    def save(self, file_name):
        with open(file_name, "w", encoding="utf-8") as file:
            data = {
                "alpha": self.alpha,
                "dictionary": self.dictionary,
                "labels": self.labels,
                "labels_count": self.labels_count,
                "size": self.size,
                "word_probability": self.word_probability,
            }

            json.dump(data, file)

    def load(file_name):
        with open(file_name, "r") as file:
            data = json.load(file)

        clf = NaiveBayesClassifier()
        clf.alpha = data["alpha"]
        clf.morph = pymorphy2.MorphAnalyzer()
        clf.dictionary = data["dictionary"]
        clf.labels = data["labels"]
        clf.labels_count = data["labels_count"]
        clf.size = data["size"]
        clf.word_probability = data["word_probability"]

        return clf
