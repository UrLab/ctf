from django.shortcuts import render
from datetime import timedelta

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.db.models import Count
from django.utils import timezone

from users.decorators import team_required

from .forms import UserForm, CreateTeamForm
from .models import User, Team
from challenges.models import Challenge, Phase, Resolution

from itertools import accumulate


class RegistrationView(CreateView):
    form_class = UserForm
    model = User
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('post_register')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


@login_required
def join_team(request):
    if request.method == 'POST':
        if request.user.team:
            return HttpResponseForbidden("You are already in a team...")

        form = CreateTeamForm(request.POST)
        if form.is_valid():
            team = Team.objects.create(name=form.cleaned_data['name'].strip())
            request.user.team = team
            request.user.save()

            messages.add_message(request, messages.SUCCESS, 'You created your team. Now invite your team mates !')
            return HttpResponseRedirect(reverse('team'))
    else:
        form = CreateTeamForm()

    teams = Team.objects.annotate(members_count=Count('members')).order_by('-members_count')
    return render(request, 'users/join_team.html', {'teams': teams, 'form': form})


@login_required
@team_required
def show_team(request):
    # TODO : refactor get phase in a fct
    phase = Phase.objects.filter(start__lte=timezone.now(), stop__gte=timezone.now()).first()
    if not phase:
        phase = Phase.objects.filter(start__lte=timezone.now()).first()

    if phase:
        resolutions = Resolution.objects.filter(challenge__phase=phase, team=request.user.team).order_by('time').select_related('challenge')
        completed = [r.challenge for r in resolutions]
        not_completed = Challenge.objects.exclude(id__in=[c.id for c in completed]).filter(phase=phase)

        history = list(accumulate(map(lambda x: x.challenge.points, resolutions)))
        times = map(lambda x: x.time, resolutions)
        score = sum(map(lambda x: x.challenge.points, resolutions))
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
            'completed': completed,
            'not_completed': not_completed,
            'total_challenges': len(completed) + len(not_completed),
            'resolutions': resolutions,
            'history': history,
            'times': times,
            'score': score,
            'end': end,
            'ticks': ticks,
            'grid': grid
        }
    else:
        ctx = {
            'phase': phase
        }
    return render(request, 'users/show_team.html', ctx)


@login_required
def accept_invite(request, secret_key):
    if not secret_key or len(secret_key) < 10:
        return HttpResponseForbidden("Wrong key format.")
    team = get_object_or_404(Team, secret_key=secret_key)

    if request.method == 'POST':
        if team.members.count() >= 4:
            return HttpResponseForbidden("Team is full, sorry.")
        if request.user.team:
            return HttpResponseForbidden("You already have a team.")

        messages.add_message(request, messages.SUCCESS, 'You joined "%s". Welcome on board!' % team)
        request.user.team = team
        request.user.save()
        return HttpResponseRedirect(reverse('team'))
    else:
        return render(request, 'users/accept_invite.html', {'team': team})


@login_required
@team_required
def reset_team_secret(request):
    if request.method == 'POST':
        request.user.team.secret_key = ""
        request.user.team.save()

        messages.add_message(request, messages.SUCCESS, 'Your team join URL has been reset.')

        return HttpResponseRedirect(reverse('team'))
    else:
        return render(request, 'users/reset_secret.html')


@login_required
def post_register(request):
    return render(request, 'users/post_register.html')
