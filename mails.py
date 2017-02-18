import sys
sys.exit()

from django.core.mail import EmailMultiAlternatives
from users.models import User


subject = 'CTF ULB'
txt = """Good evening fellow hackers,

We hope that the CTF is going well for everyone :)
Some of you have already solved 6 different challenges but you have at least 9 more to go!

Congratz to "Nova-FFT" who is leading the race with 770 points :)

We are regularly releasing news/corrections/hints on Twitter (https://twitter.com/ctfulb)
and IRC, #ctfulb on freenode (use your favorite client or the web interface in the menu on the website).

We might also release more challenges during the qualifications if you solve the current ones too quickly ^^

Have a good (not too long) night :)
The CTF Team

PS : the dictionary should only be used for offline attacks ;)
"""
fro = 'ctf@urlab.be'

import re
# DOMAINS = ["@vub.ac.be", "@vub.be", "@ulb.ac.be"]
recipients = [u.email for u in User.objects.all()]

message = EmailMultiAlternatives(
    subject=subject,
    body=txt,
    from_email='Capture the Flag ULB <ctf@urlab.be>',
    to=['Capture the Flag ULB <ctf@urlab.be>'],
    bcc=recipients,
)
message.send()
