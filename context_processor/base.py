#coding:utf8
from check_send.models import Cartriges, PostOffices, ReceiptCartridges, Dispatch
from custom_page.models import CustomPage
from post_app2.settings import PROJECT_NAME


def global_context(request,context={}):
    context['project_name']=PROJECT_NAME
    context['admin'] = {'title':'admin','get_url':'/admin'}

    context['cartridges'] = Cartriges.objects.all()
    context['post_officess'] = PostOffices.objects.all().order_by("-name")
    context['receipt'] = ReceiptCartridges.objects.all().order_by('-date_create_add')
    context['dispaths'] = Dispatch.objects.all().order_by("-disp_date").order_by("-id")[0:100]
    context['custom_page']=CustomPage
    return context