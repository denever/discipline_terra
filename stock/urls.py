from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
# permission_required

from stock.views import ProductListView, WarningProductListView, DangerProductListView, SearchProductListView
from stock.views import ProductByCategoryListView
from stock.views import ProductDetailView
from stock.views import ProductCreateView
from stock.views import ProductUpdateView
from stock.views import ProductDeleteView

from stock.views import PackageListView
from stock.views import PackageDetailView
from stock.views import PackageCreateView
from stock.views import PackageUpdateView
from stock.views import PackageDeleteView

from stock.views import CategoryCreateView
from stock.views import CategoryDeleteView

urlpatterns = patterns('stock.views',
                       url(r'^$', login_required(ProductListView.as_view()),
                           name='stock'),

                       url(r'^products/$', login_required(ProductListView.as_view()),
                           name='products'),

                       url(r'^products/search$', login_required(SearchProductListView.as_view()),
                           name='products-search'),

                       url(r'^products/category/(?P<pk>\d+)$',
                           login_required(ProductByCategoryListView.as_view()),
                           name='products-category'),

                       url(r'^products/warning$', login_required(WarningProductListView.as_view()),
                           name='products-warning'),

                       url(r'^products/danger$', login_required(DangerProductListView.as_view()),
                           name='products-danger'),

                       url(r'^product/(?P<pk>\d+)$',
                           login_required(ProductDetailView.as_view()),
                           name='product-detail'),

                       url(r'^product_create/$',
                           login_required(ProductCreateView.as_view()),
                           name='product-create'
                           ),

                       url(r'^product_update/(?P<pk>\d+)$',
                           login_required(ProductUpdateView.as_view()),
                           name='product-edit'
                           ),

                       url(r'^product_delete/(?P<pk>\d+)$',
                           login_required(ProductDeleteView.as_view()),
                           name='product-delete'
                           ),

                       url(r'^packages/$', login_required(PackageListView.as_view()),
                           name='packages'),

                       url(r'^package/(?P<pk>\d+)$',
                           login_required(PackageDetailView.as_view()),
                           name='package-detail'),

                       url(r'^package_create/$',
                           login_required(PackageCreateView.as_view()),
                           name='package-create'
                           ),

                       url(r'^package_update/(?P<pk>\d+)$',
                           login_required(PackageUpdateView.as_view()),
                           name='package-edit'
                           ),

                       url(r'^package_delete/(?P<pk>\d+)$',
                           login_required(PackageDeleteView.as_view()),
                           name='package-delete'
                           ),

                       url(r'^category_create/$',
                           login_required(CategoryCreateView.as_view()),
                           name='category-create'
                           ),

                       url(r'^category_delete/(?P<pk>\d+)$',
                           login_required(CategoryDeleteView.as_view()),
                           name='category-delete'))
