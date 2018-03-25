# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import django
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import get_connection, EmailMultiAlternatives
from django.db import models

# Create your models here.

class BaseProperty(models.Model):
    class Meta:
        abstract=True
    comment = models.TextField(blank=True,null=True)
    date_add = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания',blank=True,null=True)
    date_change = models.DateTimeField(auto_now=True, verbose_name=u'Дата изменения', blank=True, null=True)
    
class TypeCart(BaseProperty):
    class Meta():
        verbose_name_plural = u'Типы картриджей'
        verbose_name = u'Типы картриджей'
    name=models.CharField(max_length=255, verbose_name=u'Тип картриджа')
    def __unicode__(self):
        return '%s'%self.name
    
class PostOffices(BaseProperty):
    class Meta():
        verbose_name_plural = u'Почтовое отделение'
        verbose_name = u'Почтовые отделения'
    index=models.IntegerField(verbose_name=u'Индекс')
    name=models.CharField(max_length=255,primary_key=True, unique=True ,verbose_name=u'Название отделения')
    def __unicode__(self):
        return '%s'%(self.index)

class Cartriges(BaseProperty):
    class Meta():
        verbose_name_plural = u'Картриджи'
        verbose_name = u'Картриджи'
    model = models.CharField(max_length=255, unique=True, primary_key=True, verbose_name=u'Модель картриджа')
    type=models.ForeignKey(TypeCart, verbose_name=u'Тип картриджа')
    count=models.IntegerField(verbose_name=u'Колличество',default=0)
    #month_exp=models.IntegerField(default=0)
    #type_cartridge=1
    def __unicode__(self):
        return '%s' % self.model
    '''
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Cartriges, self).save()
    '''

class Dispatch(BaseProperty):
    class Meta():
        verbose_name_plural = u'Отправки'
        verbose_name = u'Отправки'
    post_office=models.ForeignKey(PostOffices ,verbose_name=u'Отделение')
    model=models.ForeignKey(Cartriges,verbose_name=u'Модель картриджа')
    amount=models.IntegerField(verbose_name=u'Колличество')
    disp_date=models.DateField(default=django.utils.timezone.now,verbose_name=u'Дата отправки')
    status = models.CharField(max_length=255, verbose_name=u'Вид действия', blank=True, null=True, default=u'Отпрпавка')

    def __unicode__(self):
        return u'%s' % (self.id)

    '''
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        super(Dispatch, self).save()
       
    def delete(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        d=Cartriges.objects.get(model=self.model)
        d.count +=self.amount
        d.save()
        super(Dispatch, self).delete()
    '''

class ReceiptCartridges(BaseProperty):
    class Meta():
        verbose_name_plural = u'Приход'
        verbose_name = u'Приход'
    model = models.ForeignKey(Cartriges,verbose_name=u'Модель картриджа')
    count=models.IntegerField(verbose_name=u'Колличество')
    date_create_add = models.DateField(default=django.utils.timezone.now, verbose_name=u'Дата поступления')
    number_doc=models.CharField(max_length=255,verbose_name=u'Номер накладной',blank=True,null=True)
    status=models.CharField(max_length=255,verbose_name=u'Вид действия',blank=True,null=True,default=u'Приход')
    def __unicode__(self):
        return u'%s' % self.id

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        c=Cartriges.objects.get(model=self.model)
        c.count=c.count+self.count
        c.save()
        super(ReceiptCartridges, self).save()

def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, attach_message=None):
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection)
    if attach_message:
        mail.attach_file(attach_message)
    return mail.send()

def delete_disp(request):
    if request.GET.get('delete_id'):
        del_disp=Dispatch.objects.get(id=request.GET.get('delete_id'))
        del_disp.delete()
        return True
    return False

def create_disp(request,context={}):
    if request.POST.get('model'):
        #proverka na otsutstvie dati, esli dati netu to prisvaivaetsya segodnya
        try:
            disp_date = datetime.datetime.strptime(request.POST['date_disp'], '%Y-%m-%d')
        except:
            disp_date = datetime.datetime.strptime(django.utils.timezone.now, '%Y-%m-%d')
         #sozdanie otpravki i zapis' v bazu
        send = Dispatch(
            disp_date=disp_date,
            post_office=PostOffices.objects.get(index=request.POST['post_office']),
            model=Cartriges.objects.get(model=request.POST['model']),
            amount=request.POST['amount'],)
        send.save()

        #c=Cartriges.objects.get(model=request.POST['model'])
        #c.count -=int(request.POST['amount'])
        #c.save()

        return True
    return False
