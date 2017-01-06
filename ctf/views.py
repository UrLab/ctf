from django.shortcuts import render
from django.db.models import Sum, Max
from django.db.models.functions import Coalesce
from django.utils import timezone

from users.models import Team, Phase


def home(request):
    context = {}
    return render(request, 'ctf/home.html', context)


def scoreboard(request):
    context = {}

    teams = Team.objects.all().annotate(points=Coalesce(Sum("resolution__challenge__points"), 0)).annotate(last=Max("resolution__time")).order_by("-points", "-last").prefetch_related("members")
    context["teams"] = teams

    # TODO : refactor get phase in a fct
    phase = Phase.objects.filter(start__lte=timezone.now(), stop__gte=timezone.now()).first()
    if not phase:
        phase = Phase.objects.filter(start__lte=timezone.now()).first()
    context["phase"] = phase

    return render(request, 'ctf/scoreboard.html', context)
