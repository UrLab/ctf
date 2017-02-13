import sys
sys.exit()

from django.core.mail import EmailMultiAlternatives
from users.models import User


subject = 'CTF ULB : last minute informations'
txt = """
Hello fellow hackers!

tl;dr : The qualifiers start at 17h00 GMT+1 on friday (17/02). Be ready !

Brace yourselves, the CTF qualifiers are coming !
Here are the last minute informations : The online qualifiers will begin on this friday (17/02) at 17h00 GMT+1 and will finish at the same time on monday the 20th.

Please note that not every challenge will be released at the beginning of the round so please follow our Twitter account (https://twitter.com/ctfulb) to be notified of new challenges and hints! (Or check regularly the website.)

The top 10 teams of the qualifiers will be invited to the finals and will be given the rights to compete for the first place and win some nice prizes. (The location of the finals is still kept secret).

Here is a quick reminder of the rules:
 - Do not tamper with the server or try to cheat (the server will be monitored)
 - Do not share flags with other teams
 - Do not listen to other teams of intercept their communications
 - Do not bruteforce the platform
 - Violations of the rules will result in the immediate exclusion of your team
 - You must be a student to participate in the challenge
 - You must be a student of ULB or VUB to participate in the finals (we will check your academic email). If you are not eligible, you can still contest in the CSC BE :) (https://www.cybersecuritychallenge.be/)

If you have a question feel free to ask us ! ctf@urlab.be

Good luck !
The CTF Team
"""
fro = 'ctf@urlab.be'


recipients = [u.email for u in User.objects.all()]

message = EmailMultiAlternatives(
    subject=subject,
    body=txt,
    from_email='Capture the Flag ULB <ctf@urlab.be>',
    to=['Capture the Flag ULB <ctf@urlab.be>'],
    bcc=recipients,
)
message.send()
