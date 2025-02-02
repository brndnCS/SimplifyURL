from django.db import models

# Create your models here.
class myURL(models.Model):
    inputURL = models.URLField()
    simplifiedURL = models.CharField(max_length=50)