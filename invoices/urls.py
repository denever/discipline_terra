from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from invoices.views import *

urlpatterns = patterns('invoices.views',
                       # url(r'^/$', login_required(InvoicesListView.as_view()),
                       #     name='invoices'),

                       url(r'^orders/$',
                           login_required(OrderListView.as_view()),
                           name='orders'),

                       url(r'^orders/search$',
                           login_required(SearchOrderListView.as_view()),
                           name='orders-search'),

                       url(r'^payments/$',
                           login_required(PaymentListView.as_view()),
                           name='payments'),

                       url(r'^payment_create/$',
                           login_required(PaymentCreateView.as_view()),
                           name='payment-create'
                           ),

                       url(r'^payment_update/(?P<pk>\d+)$',
                           login_required(PaymentUpdateView.as_view()),
                           name='payment-edit'
                           ),

                       url(r'^payment_delete/(?P<pk>\d+)$',
                           login_required(PaymentDeleteView.as_view()),
                           name='payment-delete'
                           ),

                       url(r'^invoices/$',
                           login_required(InvoiceListView.as_view()),
                           name='invoices'),

                       url(r'^invoices/search$',
                           login_required(SearchInvoiceListView.as_view()),
                           name='invoices-search'),

                       url(r'^invoice/(?P<pk>\d+)$',
                           login_required(InvoiceDetailView.as_view()),
                           name='invoice-detail'),

                       url(r'^invoice_print/(?P<pk>\d+)$',
                           login_required(InvoicePrintView.as_view()),
                           name='invoice-print'),

                       url(r'^order/(?P<pk>\d+)$',
                           login_required(OrderDetailView.as_view()),
                           name='order-detail'),

                       url(r'^order_create/$',
                           login_required(OrderCreateView.as_view()),
                           name='order-create'
                           ),

                       url(r'^order_update/(?P<pk>\d+)$',
                           login_required(OrderUpdateView.as_view()),
                           name='order-edit'
                           ),

                       url(r'^order_delete/(?P<pk>\d+)$',
                           login_required(OrderDeleteView.as_view()),
                           name='order-delete'
                           ),

                       # url(r'^order_invoice/(?P<pk>\d+)$',
                       #     login_required(OrderInvoiceView.as_view()),
                       #     name = 'order-invoice'
                       #     ),

                       url(r'^order_invoice/(?P<order>\d+)$',
                           login_required(InvoiceCreateView.as_view()),
                           name='order-invoice'
                           ),

                       url(r'^order/(?P<order>\d+)/item_create/$',
                           login_required(ItemCreateView.as_view()),
                           name='item-create'
                           ),

                       url(r'^order/(?P<order>\d+)/item_update/(?P<pk>\d+)$',
                           login_required(ItemUpdateView.as_view()),
                           name='item-edit'
                           ),

                       url(r'^order/(?P<order>\d+)/item_delete/(?P<pk>\d+)$',
                           login_required(ItemDeleteView.as_view()),
                           name='item-delete'
                           ),

                       url(r'^headings/$',
                           login_required(HeadingListView.as_view()),
                           name='headings'),

                       url(r'^heading/(?P<pk>\d+)$',
                           login_required(HeadingDetailView.as_view()),
                           name='heading-detail'),

                       url(r'^heading_create/$',
                           login_required(HeadingCreateView.as_view()),
                           name='heading-create'
                           ),

                       url(r'^heading_update/(?P<pk>\d+)$',
                           login_required(HeadingUpdateView.as_view()),
                           name='heading-edit'
                           ),

                       url(r'^heading_delete/(?P<pk>\d+)$',
                           login_required(HeadingDeleteView.as_view()),
                           name='heading-delete'
                           ))
