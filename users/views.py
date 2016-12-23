from django.shortcuts import render

# Create your views here.
from .forms import UserForm
from .models import User, Team
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

from users.decorators import team_required


def register_new_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserForm()
    return render(request, 'users/registration.html', {'form': form})


@login_required
def join_team(request):
    return render(request, 'users/join_team.html')


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
