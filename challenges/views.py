from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from .models import Challenge, Category, Resolution

# Create your views here.
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

def flag(request, pk):
    if 'flag' not in request.POST:
        return HttpResponseBadRequest("Missing parameter flag.")
    challenge = get_object_or_404(Challenge, pk=pk)
    attempt = request.POST['flag'].strip()
    if attempt != challenge.flag:
        messages.add_message(request, messages.ERROR, "Ce n'est pas le bon flag.")
    else:
        team = request.user.team
        teams = map(lambda x:x.team, challenge.resolution_set.all())
        if team not in teams:
            messages.add_message(request, messages.SUCCESS, "Félicitation, vous avez réussi ce challenge.")
            Resolution.objects.create(challenge=challenge, team=team)
        else:
            messages.add_message(request, messages.INFO, "Vous aviez déjà résolu ce challenge.")
    return HttpResponseRedirect(reverse('detail', args=[challenge.id]))
