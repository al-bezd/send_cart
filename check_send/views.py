# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime


import django
import xlwt as xlwt
from django.core import mail
from django.core.mail import message, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.encoding import python_2_unicode_compatible

from check_send.forms import DatePickerForm
from check_send.models import Cartriges, PostOffices, Dispatch, ReceiptCartridges, send_mail
from custom_page.models import get_settings_custom_file
from post_app2.settings import MEDIA_ROOT
from post_app2.settings import MEDIA_URL
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def index(request,templ_path='send_cart/index.html',context = {}):
    if request.POST.get('model'):
        #proverka na otsutstvie dati, esli dati netu to prisvaivaetsya segodnya
        try:
            disp_date = datetime.datetime.strptime(request.POST['date_disp'], '%Y-%m-%d')
        except:
            disp_date = datetime.datetime.strptime(django.utils.timezone.now, '%Y-%m-%d')
        send = Dispatch(
            disp_date=disp_date,
            post_office=PostOffices.objects.get(index=request.POST['post_office']),
            model=Cartriges.objects.get(model=request.POST['model']),
            amount=request.POST['amount'],)
        send.save()
        c=Cartriges.objects.get(model=request.POST['model'])
        c.count -=int(request.POST['amount'])
        c.save()
    context['form_date_picker']=DatePickerForm()
    response=render(request,templ_path,context)
    return response

def send_report(request):
    form = DatePickerForm(request.GET)
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





