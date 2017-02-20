import sys
sys.exit()

from django.core.mail import EmailMultiAlternatives
from users.models import User


subject = 'CTF ULB: New challenges'
txt = """Good morning!

The night has been rough and the competition is strong!
If you are stuck on some challenges, we have some good news for you, we just released a bunch of new challenges :)

Two of those challenges have been written by EY, our sponsor.
We would like to thank them a lot for their help and for the prizes they are going to give to the best of you.

With love,
The CTF team

PS : don't try "FLAGFLAGFLAG", it's only a placeholder, not a real flag ^^
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
