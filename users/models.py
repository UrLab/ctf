from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.signing import Signer

import string
import random

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
        aff = Affiliation.objects.first()
        if not aff:
            aff = Affiliation.objects.create(name="Master en Informatique ULB")
        return self._create_user(username, email, password, is_superuser=True, affiliation=aff, **extra_fields)

    def get_by_natural_key(self, username):
        # makes user matching case insensitive
        return self.get(username__iexact=username)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Utilisateur'

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    objects = CustomUserManager()

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)

    team = models.ForeignKey('users.Team', related_name='members', blank=True, null=True)
    affiliation = models.ForeignKey('users.Affiliation')

    is_active = models.BooleanField(default=True)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

    def proof_token(self):
        signer = Signer()
        return signer.sign(self.username)


class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    secret_key = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def score(self):
        resolutions = self.resolution_set.all()
        score = 0
        for resolution in resolutions:
            score += resolution.challenge.points
        return score

    @property
    def last_validation(self):
        resolutions = self.resolution_set.order_by('-time')
        if len(resolutions) > 0:
            return resolutions[0].time
        else:
            return None

    @property
    def affiliations(self):
        return set([m.affiliation for m in self.members.all()])

    def save(self, *args, **kwargs):
        if not self.secret_key:
            self.secret_key = Team.generate_secret_key()
        return super(Team, self).save(*args, **kwargs)

    @classmethod
    def generate_secret_key(cls):
        pool = string.ascii_letters + string.digits
        return ''.join([random.choice(pool) for _ in range(30)])

    def join_url(self):
        return "%s%s" % (
            settings.ROOT_URL,
            reverse('accept_invite', args=[self.secret_key])
        )


class Affiliation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
