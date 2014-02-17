from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from customers.views import *

urlpatterns = patterns('customers.views',
                       url(r'^customers/$', login_required(CustomerListView.as_view()),
                           name='customers'),

                       url(r'^customers/search$', login_required(SearchCustomerListView.as_view()),
                           name='customers-search'),

                       url(r'^customer/(?P<pk>\d+)$',
                           login_required(CustomerDetailView.as_view()),
                           name = 'customer-detail'),

                       url(r'^customer_create/$',
                           login_required(CustomerCreateView.as_view()),
                           name = 'customer-create'
                           ),

                       url(r'^customer_update/(?P<pk>\d+)$',
                           login_required(CustomerUpdateView.as_view()),
                           name = 'customer-edit'
                           ),

                       url(r'^customer_delete/(?P<pk>\d+)$',
                           login_required(CustomerDeleteView.as_view()),
                           name = 'customer-delete'
                           ),
                   )
