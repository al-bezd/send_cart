# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime


import django
import xlwt as xlwt
from django.core import mail, serializers
from django.core.mail import message, EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

from check_send.forms import DatePickerForm, DatePickerSendForm, DispFilter
from check_send.models import Cartriges, PostOffices, Dispatch, ReceiptCartridges, send_mail, delete_disp, create_disp
from custom_page.forms import get_settings_custom_file
from post_app2.settings import MEDIA_ROOT
from post_app2.settings import MEDIA_URL
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def index(request,templ_path='send_cart/index.html',context = {}):
    qs = Dispatch.objects.all().order_by("-disp_date").order_by("-id")[0:100]
    context['dispaths2'] = serializers.serialize('json', qs)
    context['dispatch_filter_form'] = DispFilter()
    form_disp_filt = DispFilter(request.GET)
    if form_disp_filt.is_valid():
        print form_disp_filt.cleaned_data
        date_begin = form_disp_filt.cleaned_data['date_begin']
        date_end = form_disp_filt.cleaned_data['date_end']
        qs = Dispatch.objects.filter(
            disp_date__gt=date_begin,
            disp_date__lt=date_end).order_by("-id")
        context['dispaths2'] = serializers.serialize('json', qs)


    form = DatePickerForm(request.GET)
    if bool(get_settings_custom_file()['receiver_email']):
        form = DatePickerSendForm(request.GET)
    context['form_date_picker']=form
    response=render(request,templ_path,context)
    return response

def send_report(request):
    form = DatePickerForm(request.GET)
    if bool(get_settings_custom_file()['receiver_email']):
        form=DatePickerSendForm(request.GET)

    form = form
    if form.is_valid():
        print form.cleaned_data
        date_begin=form.cleaned_data['date_begin']
        date_end=form.cleaned_data['date_end']


        disp = Dispatch.objects.filter(disp_date__gt=date_begin, disp_date__lt=date_end)
        wb = xlwt.Workbook()
        ws = wb.add_sheet(unicode(u'Report').decode('utf8'), cell_overwrite_ok=True)
        ws.write(0, 0, ' %s ' % (u'Отчет за период с %s по %s'%(date_begin,date_end)))
        i = 3
        ws.write(1, 0, '%s' % unicode(u'Дата отправки').encode('utf8'))
        ws.write(1, 1, '%s' % unicode(u'Модель').encode('utf8'))
        ws.write(1, 2, '%s' % unicode(u'Количество').encode('utf8'))
        ws.write(1, 3, '%s' % unicode(u'Отделение').encode('utf8'))
        for y in disp:
            ws.write(i, 0, '%s' % unicode(y.disp_date.strftime("%d.%m.%Y")).encode('utf8'))
            ws.write(i, 1, '%s' % unicode(y.model).encode('utf8'))
            ws.write(i, 2, '%s' % (unicode(y.amount).encode('utf8')))
            ws.write(i, 3, '%s' % unicode(y.post_office.name).encode('utf8'))
            i = i + 1
        excel_file_name = u'%s%s%s' % ('report', str(datetime.datetime.today().strftime("%d%m%Y_%H%M")), '.xls')
        try:
            filee='%s/%s'%(MEDIA_ROOT,excel_file_name)
        except:
            filee='%s\\%s' % (MEDIA_ROOT, excel_file_name)
        wb.save(filee)
        if form.cleaned_data['send_email']:
            subject = 'report'
            send_mail(
                subject,
                subject,
                request.user.email,
                [get_settings_custom_file()['receiver_email']],
                auth_user=get_settings_custom_file()['email_from'],
                auth_password=get_settings_custom_file()['email_from_password'],
                attach_message=filee)
        return HttpResponseRedirect('%s/%s'%(MEDIA_URL,excel_file_name))


def create_dispatch(request,context={}):
    if create_disp(request):
        return HttpResponseRedirect(reverse('api:dispatch-list',kwargs={'format':'json'}))

def delete_dispatch(request,context={}):
    if delete_disp(request):
        return HttpResponseRedirect(reverse('api:dispatch-list', kwargs={'format': 'json'}))




