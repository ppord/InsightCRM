from django.db import models
import hashlib
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class Invite(models.Model):
    invite=models.CharField(max_length=100)
    valid=models.BooleanField(default=True)

    def clean(self):
        m=hashlib.md5()
        m.update(self.ticket.encode('utf-8'))
        self.ticket=m.hexdigest()

    def __str__(self):
        vld='Использован' if not self.valid else 'Доступен'
        return ('%s - %s' % (self.ticket, vld))