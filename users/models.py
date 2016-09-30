from django.conf import settings
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, is_superuser=True, **extra_fields)

    def get_by_natural_key(self, username):
        # makes user matching case insensitive
        return self.get(username__iexact=username)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Utilisateur'

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    username = models.CharField(max_length=30, unique=True, verbose_name="nom d'utilisateur")
    email = models.EmailField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=127, blank=True)
    last_name = models.CharField(max_length=127, blank=True)

    team = models.ForeignKey('users.Team', related_name='members', blank=True, null=True)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

class Team(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

    @property
    def score(self):
        resolutions = self.resolution_set.order_by('-time')
        last_time = resolutions[0].time
        score = 0
        for resolution in resolutions:
            score += resolution.challenge.points
        return (score, last_time)
