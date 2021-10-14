from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=1000, default='')
    author = models.CharField(max_length=1000, default='')
    labels = models.CharField(max_length=1000, default='')
    description = models.TextField(default='')
    image_link = models.CharField(max_length=1000, default='')
    image_height = models.IntegerField(default=200)
    image_width = models.IntegerField(default=200)
    review = models.TextField(default='')
    book_link = models.CharField(max_length=1000, default='')
    category = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name
