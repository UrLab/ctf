import sys
sys.exit()

from django.core.mail import EmailMultiAlternatives
from users.models import User


subject = 'CTF ULB : [important] non-academic email'
txt = """
Hello fellow hackers!

We see that you registered on https://ctf.ulb.ac.be with a non-academic email.
As we said in the rules, the event is only accessible to students of the ULB (and VUB) and this is for 2 main reasons :

 - We want to leave a chance to everybody to compete and if we let compete professionals, young students don't stand a chance
 - We do not have enough resources to organize a huge challenge beyond ULB walls

Thus we would like to verify that you are indeed a student.
Could you confirm it by replying with your academic address, real first name and last name ?
(And if possible your proof token that is available on the bottom right corner at https://ctf.ulb.ac.be/accounts/team)

Failing to do so will result in your account being
The CTF Team
"""
fro = 'ctf@urlab.be'

import re
DOMAINS = ["@vub.ac.be", "@vub.be", "@ulb.ac.be"]
recipients = [u.email for u in User.objects.all() if re.search("@[\w.]+", u.email).group() not in DOMAINS]

message = EmailMultiAlternatives(
    subject=subject,
    body=txt,
    from_email='Capture the Flag ULB <ctf@urlab.be>',
    to=['Capture the Flag ULB <ctf@urlab.be>'],
    bcc=recipients,
)
message.send()
