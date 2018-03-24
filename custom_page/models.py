#coding:utf8
from __future__ import unicode_literals

import json, io

from django import forms

from custom_page.settings import PATH_TO_SETTINGS_FILE

false=False
true=True

class CustomPage(object):
    title='Опции'
    url='admin-custom-page/'

class CustomPageForm(forms.Form):
    help_text_from_receiver_email='Для отправки по почте это поле должно быть заполненно!'
    receiver_email=forms.EmailField(
        label='email получателя',
        required=False,
        widget=forms.TextInput(attrs={'title': help_text_from_receiver_email}))
    email_from=forms.EmailField(label='email отправителя',required=False)
    email_from_password=forms.CharField(label='пароль для авторизации на почте',widget=forms.PasswordInput,required=False)
    email_host=forms.CharField(label='Хост',required=False,widget=forms.TextInput(attrs={'title':'Пример: smtp.yandex.ru'}))
    email_port=forms.CharField(label='Порт',required=False)
    email_use_ssl=forms.BooleanField(label='email_use_ssl',required=False,help_text='необходимо для yandex')
    email_use_tsl=forms.BooleanField(label='email_use_tsl',required=False,help_text='необходимо для google')

def get_settings_custom_file():
    try:
        with io.open(PATH_TO_SETTINGS_FILE, encoding='utf8') as file:
            settings_write = json.load(file)
    except:
        settings_write={}
    return settings_write