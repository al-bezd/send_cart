#coding:utf8
from django.conf.urls import url, include
from django.contrib.auth.decorators import user_passes_test
from rest_framework.urlpatterns import format_suffix_patterns
from check_send import views
from check_send.views import send_report
from custom_page.forms import CustomPage
from custom_page.views import show_admin_custom_page
from api.views import UserDetail, UserList

urlpatterns = [
    url(r'^send_report/$', views.send_report),
    url(r'^%s'%CustomPage.url,
        user_passes_test(lambda u: u.is_superuser)(show_admin_custom_page),
        name='show_admin_custom_page'),
    url(r'^create_dispatch$', views.create_dispatch),
    url(r'^delete_dispatch$', views.delete_dispatch),


]

urlpatterns +=[url(r'^api/', include('api.urls', namespace='api')),]
urlpatterns.append(url(r'^$', views.index))

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])