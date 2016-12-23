from django.shortcuts import render

# Create your views here.
from .forms import UserForm
from .models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

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
