from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=1000)

class Challenge(models.Model):
    title = models.CharField(max_length=1000)
    decription = models.TextField()
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True)
    category = models.ForeignKey('Category')
    points = models.PositiveSmallIntegerField()

class Hint(models.Model):
    text = models.TextField()
    challenge = models.ForeignKey('Challenge')
