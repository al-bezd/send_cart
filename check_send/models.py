# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django
from django.db import models

# Create your models here.

class Comment(models.Model):
    class Meta:
        abstract=True
    comment = models.TextField(blank=True,null=True)
    date_add = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания',blank=True,null=True)
    
class TypeCart(Comment):
    name=models.CharField(max_length=255, unique=False, verbose_name=u'Тип картриджа')
    def __unicode__(self):
        return '%s'%(self.name)
    
class PostOffices(Comment):
    class Meta():
        verbose_name_plural = u'Почтовое отделение'
        verbose_name = u'Почтовые отделения'
    index=models.IntegerField(unique=False, verbose_name=u'Индекс')
    name=models.CharField(max_length=255,primary_key=True, unique=True ,verbose_name=u'Название отделения')
    def __unicode__(self):
        return '%s'%(self.index)

class Cartriges(Comment):
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
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Cartriges, self).save()

class Dispatch(Comment):
    class Meta():
        verbose_name_plural = u'Отправки-'
        verbose_name = u'Отправки-'
    post_office=models.ForeignKey(PostOffices ,verbose_name=u'Отделение')
    model=models.ForeignKey(Cartriges,verbose_name=u'Модель картриджа')
    amount=models.IntegerField(verbose_name=u'Колличество')
    #date_disp_create = models.DateField(auto_now_add=True,verbose_name=u'Дата создания')
    disp_date=models.DateField(default=django.utils.timezone.now,verbose_name=u'Дата отправки')
    status = models.CharField(max_length=255, verbose_name=u'Вид действия', blank=True, null=True, default=u'Отпрпавка')

    def __unicode__(self):
        return u'%s' % (self.id)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        #d=CartridgesSendChecker.objects.get(model=self.model)
        #d.count=int(d.count)-int(self.amount)
        #d.save()
        super(Dispatch, self).save()
    def delete(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        d=Cartriges.objects.get(model=self.model)
        d.count +=self.amount

        #d.count=int(d.count)-int(self.amount)
        d.save()
        super(Dispatch, self).delete()

class ReceiptCartridges(Comment):
    class Meta():
        verbose_name_plural = u'Приход'
        verbose_name = u'Приход'
    model = models.ForeignKey(Cartriges,verbose_name=u'Модель картриджа')
    count=models.IntegerField(verbose_name=u'Колличество')
    #date_add=models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    date_create_add = models.DateField(default=django.utils.timezone.now, verbose_name=u'Дата поступления')
    number_doc=models.CharField(max_length=255,verbose_name=u'Номер накладной',blank=True,null=True)
    status=models.CharField(max_length=255,verbose_name=u'Вид действия',blank=True,null=True,default=u'Приход')
    def __unicode__(self):
        return u'%s' % (self.id)
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        c=Cartriges.objects.get(model=self.model)
        c.count=c.count+self.count
        c.save()
        super(ReceiptCartridges, self).save()
