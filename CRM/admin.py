from django.contrib import admin
from .models import Invite
# Register your models here.

class InviteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Invite, InviteAdmin)