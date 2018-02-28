# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import django
import xlwt as xlwt
from django.shortcuts import render
from django.utils.encoding import python_2_unicode_compatible
from check_send.models import Cartriges, PostOffices, Dispatch, ReceiptCartridges
from post_app2.settings import MEDIA_ROOT
from post_app2.settings import MEDIA_URL
import sys
reload(sys)
sys.setdefaultencoding('utf8')
templ_path='send_cart/index.html'
context={}
def index(request):
    context['cartridges'] = Cartriges.objects.all()
    context['post_officess'] = PostOffices.objects.all().order_by("-name")
    context['dispaths']=Dispatch.objects.all().order_by("-disp_date").order_by("-id")[0:100]
    context['receipt']=ReceiptCartridges.objects.all().order_by('-date_create_add')
    if request.POST.get('model'):
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
    if request.POST.get('month') or request.POST.get('year'):
        month = request.POST['month']
        year = request.POST['year']
        disp = Dispatch.objects.filter(disp_date__year=year).filter(disp_date__month=month).exclude(status=False).order_by('disp_date').order_by('-model')
        wb = xlwt.Workbook()
        ws = wb.add_sheet(unicode(u'Report').decode('utf8'), cell_overwrite_ok=True)
        ws.write(0, 0, ' %s %s.%s' % (u'Отчет за ',request.POST['month'],request.POST['year']))
        i=3
        ws.write(1, 0, '%s' % unicode(u'Дата отправки').encode('utf8'))
        ws.write(1, 1, '%s' % unicode(u'Модель').encode('utf8'))
        ws.write(1, 2, '%s' % unicode(u'Количество').encode('utf8'))
        ws.write(1, 3, '%s' % unicode(u'Отделение').encode('utf8'))
        for y in disp:
            ws.write(i, 0, '%s' % unicode(y.disp_date.strftime("%d.%m.%Y")).encode('utf8'))
            ws.write(i, 1, '%s' % unicode(y.model).encode('utf8'))
            ws.write(i, 2, '%s' % (unicode(y.amount).encode('utf8')))
            ws.write(i, 3, '%s' % unicode(y.post_office.name).encode('utf8'))
            i=i+1
        excel_file_name = u'%s%s%s%s' % (MEDIA_URL, 'report', str(datetime.datetime.today().strftime("%d%m%Y_%H%M")), '.xls')
        wb.save(u'%s%s%s%s' % (MEDIA_ROOT,'report', str(datetime.datetime.today().strftime("%d%m%Y_%H%M")), '.xls'))
        context['report_file'] = excel_file_name
    response=render(request,templ_path,context)
    return response


