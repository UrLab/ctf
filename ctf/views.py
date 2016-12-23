from django.shortcuts import render
from users.models import Team

def home(request):
    context = {}
    return render(request, 'ctf/home.html', context)

def scoreboard(request):
    context = {}

    teams = Team.objects.all()
    teams = sorted(teams, key=lambda x: (-x.score, x.last_validation))
    context["teams"] = teams

    return render(request, 'ctf/scoreboard.html', context)
