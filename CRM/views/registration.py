#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

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
            return render_to_response('anonymous/info.html',
                                      {'message': 'На указанный адрес выслана ссылка для продолжения регистрации'},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('anonymous/info.html',
                                      {'message': 'Не введен адрес электронной почты'})

    except:
        return render_to_response('anonymous/info.html',
                                  {'message': 'No email field in request - %s' % (request.POST['email_reg'])})


def register_user(request):
    if request.method == 'GET':
        if not 'invite' in request.GET:
            return render_to_response('anonymous/info.html',
                                      {'message' : 'Не указан код регистрации'})
        try:
            invite = Invite.objects.get(invite=request.GET['invite'])
        except:
            return render_to_response('anonymous/info.html',
                                      {'message' : 'Код регистрации неверен или уже использован'})
        if not invite.valid:
            return render_to_response('anonymous/info.html',
                                      {'message' : 'Код регистрации неверен или уже использован'})
        data = {}
        data['email'] = invite.email
        data['invite'] = invite.invite
        data['username'] = invite.email
        return render_to_response('anonymous/register.html', data, context_instance=RequestContext(request))
    elif request.method == 'POST':
        form = User_form(data=request.POST)
        if form.is_valid():
            form.save()
            invite = Invite.objects.get(invite=request.POST['invite'])
            invite.valid = False
            invite.save()
            return render_to_response('anonymous/info.html',
                                      {'message' : 'Пользователь успешно зарегистрирован'})
        else:
            return render_to_response('anonymous/info.html',
                                      {'message' : 'Ошибка регистрации пользователя'})
    else:
        return render_to_response('anonymous/info.html',
                                  {'message' : 'Неподдерживаемый метод - %s' % request.method})

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
        try:
            username = User.objects.get(email=usermail).username
        except:
            return render_to_response('anonymous/info.html', {'message' : 'Неверный адрес электронной почты или пароль!'}, context_instance=RequestContext(request))

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render_to_response('anonymous/info.html',
                                          {'message': 'Пользователь заблокирован. Обратитесь к администратору.'}, context_instance=RequestContext(request))
        else:
            return render_to_response('anonymous/info.html', {'message' : 'Неверный адрес электронной почты или пароль!'}, context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')