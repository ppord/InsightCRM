from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from ..models import Invite
from ..forms import User_form
import random
import string
from django.core.mail import send_mail
import simplejson


def send_register_mail(request):
    try:
        if (request.POST['email'] is not None) and (request.POST['email'] != ''):
            invite = Invite()
            invite.email = request.POST['email']
            randomsalt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            invite.invite = '%s%s' % (request.POST['email'], randomsalt)
            invite.valid = True
            invite.clean()
            invite.save()
            send_mail('InsightCMS', 'http://testcloud.ru/register/?invite=%s' % invite.invite,
                      'robot@testcloud.ru', [request.POST['email']])
            return render_to_response('info.html',
                                      {'infomsg': 'Email sended.'},
                                      context_instance=RequestContext(request))
        else:
            return HttpResponse('Blank email field')

    except:
        print('error')
        return HttpResponse('No email field in request')


def register_user(request):
    if request.method == 'GET':
        if (request.GET['invite'] is not None) and (request.GET['invite'] != ''):
            try:
                invite = Invite.objects.get(invite=request.GET['invite'])
                if invite.valid:
                    return render_to_response('register.html', {'invite': invite.invite, 'email': invite.email},
                                              context_instance = RequestContext(request))
                else:
                    return render_to_response('info.html', {'infomsg': 'Введен использованный код регистрации'},
                                              context_instance = RequestContext(request))
            except:
                return render_to_response('info.html', {'infomsg': 'Введен несуществующий код регистрации'},
                                          context_instance = RequestContext(request))
        return render_to_response('info.html', {'infomsg': 'Не указан код регистрации.'},
                                  content_type = "application/json", context_instance = RequestContext(request))

    else:
        form = User_form(data=request.POST)
        if not form.is_valid():
            response = {}
            for k in form.errors:
                response[k] = form.errors[k][0]
            return HttpResponse(simplejson.dumps({'response': response, 'result': 'error'}),
                                content_type="application/json")
        else:
            form.save()
            invite = Invite.objects.get(invite=request.POST['invite'])
            invite.valid = False
            invite.save()
            return HttpResponse(simplejson.dumps({'response': "Added", 'result': 'success'}))


def indexpage(request):
    return render_to_response('temp.html', context_instance=RequestContext(request))