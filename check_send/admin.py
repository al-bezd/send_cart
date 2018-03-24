# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from check_send.models import PostOffices, Cartriges, Dispatch, ReceiptCartridges, TypeCart

@admin.register(TypeCart)
class TypeCartAdmin(admin.ModelAdmin):
    pass

@admin.register(PostOffices)
class PostOfficesAdmin(admin.ModelAdmin):
    list_display_links = (
        'index',
        'name',
    )
    list_display = (
        'index',
        'name',
        'date_add',
    )
@admin.register(Cartriges)
class CartrigesAdmin(admin.ModelAdmin):
    list_display_links = (
        'model',
        'type',
    )
    list_display = (
        'model',
        'type',
        'count',
        'date_add',
    )
@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = (
    'post_office',
    'model',
    'amount',
    'disp_date',
    'date_add',
    'status'
    )
    list_editable = (
        'model',
        'amount',
        'disp_date',
        'status',
    )
@admin.register(ReceiptCartridges)
class ReceiptCartridgesAdmin(admin.ModelAdmin):
    list_display = (
        'model',
        'count',
        'date_add',
        'date_create_add',
        'number_doc',
        'status'

    )
    list_editable = (
        'number_doc',
    )
