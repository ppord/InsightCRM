from django.db import models
import hashlib


class Invite(models.Model):
    invite=models.CharField(max_length=100, default = '')
    valid=models.BooleanField(default=True)
    email = models.EmailField(null = False)

    def clean(self):
        m=hashlib.md5()
        m.update(self.invite.encode('utf-8'))
        self.invite=m.hexdigest()

    def __str__(self):
        vld='Used' if not self.valid else 'Available'
        return ('%s - %s' % (self.invite, vld))