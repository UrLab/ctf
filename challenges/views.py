from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone


from ratelimit.decorators import ratelimit

from .models import Challenge, Category, Resolution, Phase
from users.decorators import team_required


@login_required
def list_challenges(request):
    phase = Phase.objects.filter(start__lte=timezone.now(), stop__gte=timezone.now()).first()

    categories = Category.objects.all()
    for category in categories:
        category.this_phase_challenges = category.challenge_set.filter(phase=phase)

    ctx = {
        'phase': phase,
        'categories': categories,
    }
    return render(request, "challenges/list.html", ctx)


class DetailView(generic.DetailView):
    model = Challenge
    template_name = 'challenges/detail.html'

    def get(self, request, *args, **kwargs):
        original = super(DetailView, self).get(request, *args, **kwargs)
        if not self.object.phase or self.object.phase.start > timezone.now():
            return HttpResponseForbidden("This challenge is not yet available.")
        return original


def team_key(group, request):
    return str(request.user.team.id)


# Ratelimlit at 1 request every 2 second per team
@login_required
@team_required
@ratelimit(key=team_key, rate='1/5s')
def flag(request, pk):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return render(request, "challenges/rate_limited.html", status=429)
    if 'flag' not in request.POST:
        return HttpResponseBadRequest("Missing parameter flag.")
    challenge = get_object_or_404(Challenge, pk=pk)
    attempt = request.POST['flag'].strip()
    if attempt != challenge.flag:
        messages.add_message(request, messages.ERROR, "You had the wrong flag, sorry...")
    else:
        if not challenge.phase.start or challenge.phase.start > timezone.now() or challenge.phase.stop < timezone.now():
            return HttpResponseForbidden("This challenge is not active at the moment")
        team = request.user.team
        teams = map(lambda x: x.team, challenge.resolution_set.all())
        if team not in teams:
            messages.add_message(request, messages.SUCCESS, "Congrats, you flagged this challenge!")
            Resolution.objects.create(challenge=challenge, team=team)
        else:
            messages.add_message(request, messages.INFO, "You already flagged this challenge, nice try!")
    return HttpResponseRedirect(reverse('detail', args=[challenge.id]))
