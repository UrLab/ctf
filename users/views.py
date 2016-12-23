from django.shortcuts import render

# Create your views here.
from .forms import UserForm
from .models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def register_new_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserForm()
    return render(request, 'users/registration.html', {'form': form})


def join_team(request):
    return render(request, 'users/join_team.html')
