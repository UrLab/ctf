from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest

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


@login_required
def flag(request, pk):
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
