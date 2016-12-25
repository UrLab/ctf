from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Challenge(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True)
    category = models.ForeignKey('Category')
    points = models.PositiveSmallIntegerField()
    flag = models.CharField(max_length=255)
    phase = models.ForeignKey('Phase')

    def __str__(self):
        return self.title

    @property
    def visible_hint_set(self):
        return self.hint_set.filter(visible=True)


class Hint(models.Model):
    text = models.TextField()
    challenge = models.ForeignKey('Challenge')
    visible = models.BooleanField(default=False)

    def __str__(self):
        return "Hint for %s" % self.challenge


class Resolution(models.Model):
    challenge = models.ForeignKey('Challenge')
    team = models.ForeignKey('users.Team')
    time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("challenge", "team"))

    def __str__(self):
        return "Resolution of %s from %s" % (self.challenge, self.team)


class Phase(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(default="")

    # TODO : double check timezones
    start = models.DateTimeField()
    stop = models.DateTimeField()

    def __str__(self):
        return self.name
