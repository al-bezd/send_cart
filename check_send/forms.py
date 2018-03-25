#coding:utf8
from __future__ import unicode_literals
from django import forms

from custom_page.forms import get_settings_custom_file

class DateBeginAndEnd(forms.Form):
    widget = forms.TextInput(attrs={'style': 'display:inline-block;', 'type': 'date'})
    date_begin=forms.DateField(required=True,widget=widget,label='С')
    date_end=forms.DateField(required=True,widget=widget,label='По')


class DatePickerForm(DateBeginAndEnd):
    url='/send_report'
    id_form='seng_report_form_id'

class DatePickerSendForm(DatePickerForm):
    send_email = forms.BooleanField(
        required=False,
        label='Отправить отчет?',
        help_text='Получатель %s'%get_settings_custom_file()['receiver_email'])

class DispFilter(DateBeginAndEnd):
    url = ''
    form_id = 'dispatch_filter_form_id'
    '''on=forms.BooleanField(
        #show_hidden_initial=True,
        widget=forms.CheckboxInput(attrs={
            'checked':True,
            'hidden':True}
        )
    )'''


