from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField('作者', max_length=20)


class Book(models.Model):
    title = models.CharField('书名', max_length=100)
    authors = models.ManyToManyField(Author)
