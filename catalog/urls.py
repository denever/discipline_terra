from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from catalog.views import PriceListView
from catalog.views import PriceDetailView
from catalog.views import PriceCreateView
from catalog.views import PriceUpdateView
from catalog.views import PriceDeleteView

urlpatterns = patterns('catalog.views',
                       url(r'^$', login_required(PriceListView.as_view()),
                           name='catalog'),

                       url(r'^prices/$', login_required(PriceListView.as_view()),
                           name='prices'),

                       url(r'^price/(?P<pk>\d+)$',
                           login_required(PriceDetailView.as_view()),
                           name = 'price-detail'),

                       url(r'^price_create/$',
                           login_required(PriceCreateView.as_view()),
                           name = 'price-create'
                           ),

                       url(r'^price_update/(?P<pk>\d+)$',
                           login_required(PriceUpdateView.as_view()),
                           name = 'price-edit'
                           ),

                       url(r'^price_delete/(?P<pk>\d+)$',
                           login_required(PriceDeleteView.as_view()),
                           name = 'price-delete'
                           ),
)
