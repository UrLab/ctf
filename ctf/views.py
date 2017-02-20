from datetime import timedelta
from django.shortcuts import render
from django.db.models import Sum, Max
from django.db.models.functions import Coalesce
from django.utils import timezone

from users.models import Team
from challenges.models import Phase, Resolution

from itertools import groupby, accumulate


def home(request):
    context = {}
    return render(request, 'ctf/home.html', context)


def rules(request):
    context = {}
    return render(request, 'ctf/rules.html', context)


def scoreboard(request):
    context = {}

    # TODO : refactor get phase in a fct
    phase = Phase.objects.filter(start__lte=timezone.now(), stop__gte=timezone.now()).first()
    if not phase:
        phase = Phase.objects.filter(start__lte=timezone.now()).last()
    context["phase"] = phase

    teams = Team.objects.filter(hidden=False).filter(resolution__challenge__phase=phase).annotate(points=Coalesce(Sum("resolution__challenge__points"), 0)).annotate(last=Max("resolution__time")).order_by("-points", "last").prefetch_related("members")
    context["teams"] = teams


    return render(request, 'ctf/scoreboard.html', context)


def team_stat(team):
    team, resolutions = team
    times = list(map(lambda x: x.time, resolutions))
    history = list(accumulate(map(lambda x: x.challenge.points, resolutions)))
    return (team.name, times, history)


def stats(request):
    # TODO : refactor get phase in a fct
    phase = Phase.objects.filter(start__lte=timezone.now(), stop__gte=timezone.now()).first()
    if not phase:
        phase = Phase.objects.filter(start__lte=timezone.now()).first()

    if phase:
        resolutions = Resolution.objects.filter(challenge__phase=phase, team__hidden=False).order_by('team_id', 'time').select_related('challenge').select_related('team')
        teams = map(lambda x: (x[0], list(x[1])), groupby(resolutions, lambda x:x.team))
        teams = map(team_stat, teams)

        end = min(timezone.now(), phase.stop)

        grid = [phase.start + i * timedelta(days=1) for i in range(-1, (end - phase.start).days + 2)]

        def round_time(dt):
            return dt.replace(minute=0, second=0)

        N_TICKS = 15 # NOQA
        tick_interval = (end - phase.start) / N_TICKS
        tick_interval = timedelta(hours=tick_interval.total_seconds() // 3600)
        ticks = [round_time(phase.start + i * tick_interval) for i in range(N_TICKS + 10)]

        ctx = {
            'phase': phase,
            'teams': list(teams),
            'end': end,
            'ticks': ticks,
            'grid': grid
        }
    else:
        ctx = {
            'phase': phase
        }
    return render(request, 'ctf/stats.html', ctx)
