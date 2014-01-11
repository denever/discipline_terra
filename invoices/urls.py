from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from invoices.views import CustomerListView, SearchCustomerListView
from invoices.views import CustomerDetailView
from invoices.views import CustomerCreateView
from invoices.views import CustomerUpdateView
from invoices.views import CustomerDeleteView

from invoices.views import OrderListView
from invoices.views import OrderDetailView
from invoices.views import OrderCreateView
from invoices.views import OrderUpdateView
from invoices.views import OrderDeleteView
from invoices.views import OrderInvoiceView

from invoices.views import ItemCreateView
from invoices.views import ItemUpdateView
from invoices.views import ItemDeleteView

from invoices.views import InvoiceListView
from invoices.views import InvoiceDetailView
from invoices.views import InvoicePrintView

urlpatterns = patterns('invoices.views',
                       # url(r'^/$', login_required(InvoicesListView.as_view()),
                       #     name='invoices'),

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

                       url(r'^orders/$', login_required(OrderListView.as_view()),
                           name='orders'),

                       url(r'^invoices$', login_required(InvoiceListView.as_view()),
                           name='invoices'),

                       url(r'^invoice/(?P<pk>\d+)$',
                           login_required(InvoiceDetailView.as_view()),
                           name = 'invoice-detail'),

                       url(r'^invoice_print/(?P<pk>\d+)$',
                           login_required(InvoicePrintView.as_view()),
                           name = 'invoice-print'),

                       url(r'^order/(?P<pk>\d+)$',
                           login_required(OrderDetailView.as_view()),
                           name = 'order-detail'),

                       url(r'^order_create/$',
                           login_required(OrderCreateView.as_view()),
                           name = 'order-create'
                           ),

                       url(r'^order_update/(?P<pk>\d+)$',
                           login_required(OrderUpdateView.as_view()),
                           name = 'order-edit'
                           ),

                       url(r'^order_delete/(?P<pk>\d+)$',
                           login_required(OrderDeleteView.as_view()),
                           name = 'order-delete'
                           ),

                       url(r'^order_invoice/(?P<pk>\d+)$',
                           login_required(OrderInvoiceView.as_view()),
                           name = 'order-invoice'
                           ),

                       # url(r'^items/$', login_required(ItemListView.as_view()),
                       #     name='items'),

                       # url(r'^item/(?P<pk>\d+)$',
                       #     login_required(ItemDetailView.as_view()),
                       #     name = 'item-detail'),

                       url(r'^order/(?P<order>\d+)/item_create/$',
                           login_required(ItemCreateView.as_view()),
                           name = 'item-create'
                           ),

                       url(r'^order/(?P<order>\d+)/item_update/(?P<pk>\d+)$',
                           login_required(ItemUpdateView.as_view()),
                           name = 'item-edit'
                           ),

                       url(r'^order/(?P<order>\d+)/item_delete/(?P<pk>\d+)$',
                           login_required(ItemDeleteView.as_view()),
                           name = 'item-delete'
                           ),
)
