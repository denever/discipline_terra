from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from stock.views import ProductListView
from stock.views import ProductDetailView
from stock.views import ProductCreateView
from stock.views import ProductUpdateView
from stock.views import ProductDeleteView

from stock.views import PackageListView
from stock.views import PackageDetailView
from stock.views import PackageCreateView
from stock.views import PackageUpdateView
from stock.views import PackageDeleteView

urlpatterns = patterns('stock.views',
                       url(r'^$', login_required(ProductListView.as_view()),
                           name='stock'),

                       url(r'^product/(?P<pk>\w+)$',
                           login_required(ProductDetailView.as_view()),
                           name = 'product-detail'),

                       url(r'^product_create/$',
                           login_required(ProductCreateView.as_view()),
                           name = 'product-create'
                           ),

                       url(r'^product_update/(?P<pk>\w+)$',
                           login_required(ProductUpdateView.as_view()),
                           name = 'product-edit'
                           ),

                       url(r'^product_delete/(?P<pk>\w+)$',
                           login_required(ProductDeleteView.as_view()),
                           name = 'product-delete'
                           ),

                       url(r'^package/(?P<pk>\w+)$',
                           login_required(PackageDetailView.as_view()),
                           name = 'package-detail'),

                       url(r'^package_create/$',
                           login_required(PackageCreateView.as_view()),
                           name = 'package-create'
                           ),

                       url(r'^package_update/(?P<pk>\w+)$',
                           login_required(PackageUpdateView.as_view()),
                           name = 'package-edit'
                           ),

                       url(r'^package_delete/(?P<pk>\w+)$',
                           login_required(PackageDeleteView.as_view()),
                           name = 'package-delete'
                           ),
)
