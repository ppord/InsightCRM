from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
        if (request.POST['email_reg'] is not None) and (request.POST['email_reg'] != ''):
            invite = Invite()
            invite.email = request.POST['email_reg']
            randomsalt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            invite.invite = '%s%s' % (request.POST['email_reg'], randomsalt)
            invite.valid = True
            invite.clean()
            invite.save()
            send_mail('InsightCRM', 'http://testcloud.ru/register/?invite=%s' % invite.invite,
                      'robot@testcloud.ru', [request.POST['email_reg']])
            return render_to_response('info.html',
                                      {'infomsg': 'Email sended.'},
                                      context_instance=RequestContext(request))
        else:
            return HttpResponse('Blank email field')

    except:
        print('error')
        return HttpResponse('No email field in request - %s' % (request.POST['email_reg']))


def register_user(request):
    if request.method == 'GET':
        if (request.GET['invite'] is not None) and (request.GET['invite'] != ''):
            try:
                invite = Invite.objects.get(invite=request.GET['invite'])
                if invite.valid:
                    return render_to_response('anonymous/register.html', {'invite': invite.invite, 'email': invite.email},
                                              context_instance = RequestContext(request))
                else:
                    return render_to_response('anonymous/info.html', {'infomsg': 'Введен использованный код регистрации'},
                                              context_instance = RequestContext(request))
            except:
                return render_to_response('anonymous/info.html', {'infomsg': 'Введен несуществующий код регистрации'},
                                          context_instance = RequestContext(request))
        return render_to_response('anonymous/info.html', {'infomsg': 'Не указан код регистрации.'},
                                  content_type = "application/json", context_instance = RequestContext(request))

    else:
        dt = {}
        dt['email'] = request.POST['email']
        username = dt['email']
        username.replace('@', '').replace('.', '').replace('+', '')
        dt['username'] = username
        dt['csrfmiddlewaretoken'] = request.POST['csrfmiddlewaretoken']
        dt['password'] = request.POST['password']
        # request.POST['username'] = request.POST['email']
        form = User_form(data=dt)

        if not form.is_valid():
            response = {}
            for k in form.errors:
                response[k] = form.errors[k][0]
            return HttpResponse(dt)
        else:
            form.save()
            invite = Invite.objects.get(invite=request.POST['invite'])
            invite.valid = False
            invite.save()
            return HttpResponse(simplejson.dumps({'response': "Added", 'result': 'success'}))


def indexpage(request):
    if request.user.is_authenticated():
        return render_to_response('app/index.html', context_instance=RequestContext(request))
    else:
        return render_to_response('anonymous/index.html', context_instance=RequestContext(request))


def user_login(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/')
    else:
        usermail = request.POST['email']
        password = request.POST['password']
        username = User.objects.get(email=usermail).username
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render_to_response('info.html',
                                          {'infomsg': 'Пользователь не активирован. Обратитесь к администратору.'}, context_instance=RequestContext(request))

        else:
            return render_to_response('info.html', {'infomsg': 'Неправильный пароль!'})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')