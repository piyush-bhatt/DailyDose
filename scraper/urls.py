from django.conf.urls import url
from . import views

app_name = 'scraper'
urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^show/(?P<pk>\w+)/(?P<sub>\w+)/$', views.display, name='display'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^forgotPwd/$', views.forgotPwd, name='forgotPwd'),
    url(r'^profile/(?P<pk>\w+)/$', views.profile, name='profile'),
    url(r'^addSubreddit/(?P<pk>\w+)/$', views.addSubreddit, name='addSubreddit'),
    url(r'^deleteSubreddit/(?P<pk>\w+)/(?P<sub>\w+)$', views.deleteSubreddit, name='deleteSubreddit'),
]