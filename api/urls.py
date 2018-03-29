from django.conf.urls import url

from api.views import UserList, UserDetail, PostDetail, PostList, CartrigesList, CartridgieDetail, DispatchList, \
    DispatchDetail

urlpatterns=[
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'^post-offices/$', PostList.as_view(), name='postoficce-list'),
    url(r'^post-offices/(?P<index>\d+)/$', PostDetail.as_view(), name='postoficce-detail'),
    url(r'^cartridgies/$', CartrigesList.as_view(), name='cartridgie-list'),
    url(r'^cartridgies/(?P<model>\d+)/$', CartridgieDetail.as_view(), name='cartridgie-detail'),
    url(r'^dispatchs/$', DispatchList.as_view(), name='dispatch-list'),
    url(r'^dispatchs/(?P<pk>\d+)/$', DispatchDetail.as_view(), name='dispatch-detail'),
]