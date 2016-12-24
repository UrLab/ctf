from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.db.models import Count

from users.decorators import team_required

from .forms import UserForm, CreateTeamForm
from .models import User, Team


class RegistrationView(CreateView):
    form_class = UserForm
    model = User
    template_name_suffix = '_create_form'
    # TODO : redirect the user to a success page
    # TODO : maybe propose him to create a team
    # TODO : and why not a quick FAQ or introduction
    success_url = reverse_lazy('home')

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
    return render(request, 'users/show_team.html')


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
