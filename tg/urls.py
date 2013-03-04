from django.conf.urls import patterns, url

from tg import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
	url(r'^cat/(?P<category_name_url>\w+)', views.category, name='category'),
)
