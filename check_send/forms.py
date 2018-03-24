#coding:utf8
from __future__ import unicode_literals
from django import forms

from custom_page.models import get_settings_custom_file


class DatePickerForm(forms.Form):
    url='/send_report'
    id_form='seng_report_form_id'
    widget=forms.TextInput(attrs={'style': 'display:inline-block;','type':'date'})

    date_begin=forms.DateField(required=True,widget=widget,label='С')
    date_end=forms.DateField(required=True,widget=widget,label='По')

    if get_settings_custom_file():
        send_email=forms.BooleanField(required=False,label='Отправить отчет?')
