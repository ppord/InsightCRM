from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.edit import FormView
from ..forms import CompanyForm

class CompanyFormView(FormView):
    form_class = CompanyForm
    success_url = '/saved'


