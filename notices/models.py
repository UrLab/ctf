from django.db import models

# Create your models here.
class Notice(models.Model):
    text = models.TextField()
