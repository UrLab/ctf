from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Challenge(models.Model):
    title = models.CharField(max_length=1000)
    decription = models.TextField()
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True)
    category = models.ForeignKey('Category')
    points = models.PositiveSmallIntegerField()
    flag = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Hint(models.Model):
    text = models.TextField()
    challenge = models.ForeignKey('Challenge')

class Resolution(models.Model):
    challenge = models.ForeignKey('Challenge')
    team = models.ForeignKey('users.Team')
    time = models.DateTimeField(auto_now=True)
