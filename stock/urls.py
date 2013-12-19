from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from stock.views import ProductListView
from stock.views import ProductDetailView
from stock.views import ProductCreateView
from stock.views import ProductUpdateView
from stock.views import ProductDeleteView

urlpatterns = patterns('stock.views',
                       url(r'^$', login_required(ProductListView.as_view()),
                           name='stock'),

                       url(r'^product/(?P<pk>\w+)$',
                           login_required(ProductDetailView.as_view()),
                           name = 'product-detail'),

                       url(r'^create/$',
                           login_required(ProductCreateView.as_view()),
                           name = 'product-create'
                           ),

                       url(r'^update/(?P<pk>\w+)$',
                           login_required(ProductUpdateView.as_view()),
                           name = 'product-edit'
                           ),

                       url(r'^delete_product/(?P<pk>\w+)$',
                           login_required(ProductDeleteView.as_view()),
                           name = 'product-delete'
                           ),
)
