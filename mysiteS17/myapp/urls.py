from django.conf.urls import url
from . import views
from myapp.views import about,index

urlpatterns = [
        url(r'^$', index.as_view(),name='index'),
        url(r'^about/$', about.as_view(),name='about'),
        url(r'^(?P<course_no>\d+)/$', views.detail, name='detail'),
        url(r'^topics/$',views.topics, name='topics'),
        url(r'^addtopic/$',views.addtopic, name='addtopic'),
        url(r'^topics/(?P<topic_id>\d+)/$', views.topicdetail, name='topicdetail'),
        url(r'^register/$', views.register, name='register'),
        url(r'^user_login/$', views.user_login, name='user_login'),
        url(r'^user_logout/$', views.user_logout, name='user_logout'),
        url(r'^mycourse/$', views.mycourse, name='mycourse'),
        ]
