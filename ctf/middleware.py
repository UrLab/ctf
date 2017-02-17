from ctf.models import IPLog
from django.db import IntegrityError


class LogUserDetailsMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                ip = request.META.get('HTTP_X_FORWARDED_FOR')
                if not ip:
                    ip = request.META.get('REMOTE_ADDR')
                IPLog.objects.create(ip=ip, user=request.user)
            except IntegrityError:
                pass
