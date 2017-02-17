from django.db import models


class IPLog(models.Model):
    user = models.ForeignKey('users.user')
    ip = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("ip", "user"),)
