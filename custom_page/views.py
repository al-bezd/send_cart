# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import io
from django.contrib import messages
from django.shortcuts import render
from custom_page.models import CustomPageForm
from custom_page.settings import PATH_TO_SETTINGS_FILE

def show_admin_custom_page(request,template='custom_page/admin_custom_page.html',context={}):
    try:
        with io.open(PATH_TO_SETTINGS_FILE, encoding='utf8') as file:
            settings_write = json.load(file)
    except:
        settings_write={}

    if request.method == 'POST':
        form = CustomPageForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            settings=open(PATH_TO_SETTINGS_FILE,'w')
            settings.write(json.dumps(form.cleaned_data))
            settings.close()
            context['form'] = CustomPageForm(form.cleaned_data)
            messages.success(request, "Данные записаны")
            #messages.error(request, "Возникла ошибка")
    else:
        context['form'] = CustomPageForm(settings_write)
    return render(request, template, context)