# -*- coding: utf-8 -*- 

from django.forms import ModelForm
from ..models import Company


class CompanyForm(ModelForm):

    class Meta:
        model = Company

    def save(self, commit=True):
        company = super(CompanyForm, self).save(commit=False)
        if commit:
            company.save()
        return company