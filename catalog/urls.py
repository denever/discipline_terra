from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from catalog.views import PriceListView
from catalog.views import SearchPriceListView
from catalog.views import PriceListByCatalogView
from catalog.views import PriceDetailView
from catalog.views import PriceCreateView
from catalog.views import PriceUpdateView
from catalog.views import PriceDeleteView

from catalog.views import CatalogListView
from catalog.views import CatalogCreateView
from catalog.views import CatalogUpdateView
from catalog.views import CatalogDeleteView

urlpatterns = patterns('catalog.views',
                       url(r'^$', login_required(CatalogListView.as_view()),
                           name='catalog'),

                       url(r'^catalogs/$', login_required(CatalogListView.as_view()),
                           name='catalogs'),

                       url(r'^catalog_create/$',
                           login_required(CatalogCreateView.as_view()),
                           name = 'catalog-create'
                           ),

                       url(r'^catalog_update/(?P<pk>\d+)$',
                           login_required(CatalogUpdateView.as_view()),
                           name = 'catalog-edit'
                           ),

                       url(r'^catalog_delete/(?P<pk>\d+)$',
                           login_required(CatalogDeleteView.as_view()),
                           name = 'catalog-delete'
                           ),

                       url(r'^prices/$', login_required(PriceListView.as_view()),
                           name='prices'),

                       url(r'^prices/catalog/(?P<pk>\d+)$', login_required(PriceListByCatalogView.as_view()),
                           name='prices-catalog'),

                       url(r'^catalog/(?P<pk>\d+)/prices/search$', login_required(SearchPriceListView.as_view()),
                           name='prices-search'),

                       url(r'^price/(?P<pk>\d+)$',
                           login_required(PriceDetailView.as_view()),
                           name = 'price-detail'),

                       url(r'^catalog/(?P<pk>\d+)/price_create$',
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
