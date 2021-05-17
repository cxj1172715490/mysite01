from django.db import models


# Create your models here.
class Content(models.Model):
    title = models.CharField('标题', max_length=100)
    picture = models.FileField(upload_to='picture')
