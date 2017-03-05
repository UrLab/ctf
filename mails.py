import sys
sys.exit()

from django.core.mail import EmailMultiAlternatives
from users.models import User
from datetime import timedelta
from django.shortcuts import render
from django.db.models import Sum, Max
from django.db.models.functions import Coalesce
from users.models import Team
from challenges.models import Phase, Resolution
from users.models import User
import re
from itertools import groupby, accumulate
from challenges.models import Phase

phase = Phase.objects.get(id=2)
teams = Team.objects.filter(hidden=False).filter(resolution__challenge__phase=phase).annotate(points=Coalesce(Sum("resolution__challenge__points"), 0)).annotate(last=Max("resolution__time")).order_by("-points", "last").prefetch_related("members")[:10]
users = []
for t in teams:
    users.extend(t.members.all())

allusers = User.objects.all()
finals = users
recipients = [u.email for u in users]



subject = 'CTF ULB: Finals tomorrow!'
txt = """Good evening fellow hackers!

Tomorrow is the big day :)
As we said earlier, it will take place Monday (27/02) at the Proximus towers: Boulevard du Roi Albert II 27, 1030 Bruxelles. There are two towers, the meeting point is at the VIP entrance, not in the tower with a shop.
We will meet you at the entrance of the tower at 8h40. Please don’t be late, as we will not be able to wait there for long and if we aren’t present to escort you, you will not be able to enter. The competition will end at 17h with a small drink.
Proximus will provide a meal and drinks around noon, no need to bring your own :)

See you there !

57697468206c6f7665,
The CTF Team
"""
fro = 'ctf@urlab.be'


message = EmailMultiAlternatives(
    subject=subject,
    body=txt,
    from_email='Capture the Flag ULB <ctf@urlab.be>',
    to=['Capture the Flag ULB <ctf@urlab.be>'],
    bcc=recipients,
)
message.send()
