from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from invoices.views import CustomerListView
from invoices.views import CustomerDetailView
from invoices.views import CustomerCreateView
from invoices.views import CustomerUpdateView
from invoices.views import CustomerDeleteView

urlpatterns = patterns('invoices.views',
                       # url(r'^/$', login_required(InvoicesListView.as_view()),
                       #     name='invoices'),

                       url(r'^customers/$', login_required(CustomerListView.as_view()),
                           name='customers'),

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
