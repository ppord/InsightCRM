from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from ..models import Invite
import random
import string
from django.core.mail import send_mail



def send_register_mail(request):
    if (request.GET['email'] is not None) and (request.GET['email'] != ''):
        invite = Invite()
        invite.email = request.GET['email']
        randomsalt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        invite.invite = '%s%s' % (request.GET['email'], randomsalt)
        invite.valid = True
        invite.clean()
        invite.save()
        print(invite.invite)
        send_mail('InsightCMS', 'http://testcloud.ru/register/?invite=%s' % invite.invite,
                  'robot@testcloud.ru', [request.GET['email']])
        print('sended')
        return render_to_response('info.html',
                                  {'infomsg': 'Email sended.'},
                                  context_instance=RequestContext(request))

    else:
        print('error')
        return HttpResponse('Something wrong')


def register(request):
    #заглушка страницы регистрации
    return render_to_response('info.html',
                              {'infomsg': 'Register page'},
                              context_instance=RequestContext(request))


def indexpage(request):
    return render_to_response('index.html', context_instance=RequestContext(request))