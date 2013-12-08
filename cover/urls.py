from django.conf.urls import patterns, include, url

from cover.views import CoverView

urlpatterns = patterns('cover.views',
                       url(r'^$', CoverView.as_view(), name='cover'),
)
