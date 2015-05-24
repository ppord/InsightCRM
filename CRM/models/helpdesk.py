from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


USER_ROLES = (
    (1, _('Customer')),
    (2, _('Executor')),
)

ACTIONS = (
    (1, _('Open')),
    (2, _('Assign')),
    (3, _('Comment')),
    (4, _('Close')),
)

FILETYPES = (
    (1, _('Image')),
    (2, _('Archive')),
    (3, _('Document')),
    (4, _('Other')),
)

class Company(models.Model):
    name=models.CharField(max_length=50, verbose_name=_('Company'))
    address=models.CharField(max_length=100, verbose_name=_('Address'))
    inn=models.CharField(max_length=12, verbose_name=_('INN'))
    contact=models.CharField(max_length=50, verbose_name=_('Contact'))
    phone=models.CharField(max_length=10, verbose_name=_('Phone number'))


class Ticket(models.Model):
    customer=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Customer'), related_name='Customer')
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Executor'), related_name='Executor')
    slug=models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('ticket', kwargs={'pk': self.pk})


class Profile(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    company=models.ForeignKey(Company, verbose_name=_('Company'))
    role=models.IntegerField(verbose_name=_('User role'), choices=USER_ROLES)


class Action(models.Model):
    ticket=models.ForeignKey(Ticket, verbose_name=_('Ticket'))
    action=models.IntegerField(verbose_name=_('Action'), choices=ACTIONS)
    datetime=models.DateTimeField(verbose_name=_('Addition time'), auto_now_add=True)
    comment=models.TextField(verbose_name=_('Comment'), max_length=1000)


class BinaryObject(models.Model):
    path=models.FileField(verbose_name=_('File path'))
    action=models.ForeignKey(Action)
    filetype=models.IntegerField(verbose_name=_('File type'), choices=FILETYPES)
    description=models.TextField(verbose_name=_('Description'), max_length=200)