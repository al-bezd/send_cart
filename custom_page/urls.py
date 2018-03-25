# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test

from custom_page.forms import CustomPage
from custom_page.views import show_admin_custom_page

urlpatterns = [
    url(r'^%s'%CustomPage.url,
        user_passes_test(lambda u: u.is_superuser)(show_admin_custom_page), name='show_admin_custom_page'),
]