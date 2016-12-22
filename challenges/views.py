from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render

from ratelimit.decorators import ratelimit

from .models import Challenge, Category, Resolution


class ListView(generic.ListView):
    template_name = 'challenges/list.html'
    model = Challenge
    context_object_name = 'challenges_list'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class DetailView(generic.DetailView):
    model = Challenge
    template_name = 'challenges/detail.html'


def team_key(group, request):
    return str(request.user.team.id)


# Ratelimlit at 1 request every 2 second per team
@ratelimit(key=team_key, rate='1/5s')
@login_required
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
        team = request.user.team
        teams = map(lambda x: x.team, challenge.resolution_set.all())
        if team not in teams:
            messages.add_message(request, messages.SUCCESS, "Congrats, you flagged this challenge!")
            Resolution.objects.create(challenge=challenge, team=team)
        else:
            messages.add_message(request, messages.INFO, "You already flagged this challenge, nice try!")
    return HttpResponseRedirect(reverse('detail', args=[challenge.id]))
