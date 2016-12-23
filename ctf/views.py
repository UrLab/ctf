from django.shortcuts import render
from django.db.models import Sum, Max
from django.db.models.functions import Coalesce
from users.models import Team

def home(request):
    context = {}
    return render(request, 'ctf/home.html', context)

def scoreboard(request):
    context = {}

    teams = Team.objects.all().annotate(points=Coalesce(Sum("resolution__challenge__points"), 0)).annotate(last=Max("resolution__time")).order_by("-points", "-last").prefetch_related("members")
    context["teams"] = teams

    return render(request, 'ctf/scoreboard.html', context)
