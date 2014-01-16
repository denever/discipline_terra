from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.utils.timezone import utc
from invoices.draw_pdf import draw_pdf
from invoices.models import *

# Create your views here.
from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, SingleObjectMixin

from invoices.forms import *

class CustomerListView(ListView):
    queryset = Customer.objects.all()
    context_object_name = 'customers'
    paginate_by = 5

class SearchCustomerListView(ListView):
    model = Customer
    context_object_name = 'customers'
    paginate_by = 5
    template_name = 'invoices/customer_list.html'

    def get_queryset(self):
        query = self.request.REQUEST.get("q")
        return self.model.objects.filter(Q(surname__contains=query)| Q(name__contains=query))

class CustomerDetailView(DetailView):
    model = Customer
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    form_class = CustomerForm
    template_name = 'invoices/customer_create_form.html'
    success_url = '/invoices/customers/'

    def form_valid(self, form):
        self.customer = form.save(commit=False)
        self.customer.record_by = self.request.user.get_profile()
        self.customer.lastchange_by = self.request.user.get_profile()
        self.customer.lastchange = datetime.utcnow().replace(tzinfo=utc)
        return super(CustomerCreateView, self).form_valid(form)

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'invoices/customer_update_form.html'
    success_url = '/invoices/customers/'
    context_object_name = 'customer'

    def form_valid(self, form):
        self.customer = form.save(commit=False)
        self.customer.lastchange_by = self.request.user.get_profile()
        self.customer.lastchange = datetime.utcnow().replace(tzinfo=utc)
        self.success_url = reverse('customer-detail', args=[self.kwargs['pk']])
        return super(CustomerUpdateView, self).form_valid(form)

class CustomerDeleteView(DeleteView):
    model = Customer
    form_class = CustomerForm
    success_url = '/invoices/customers'
    context_object_name = 'customer'

class OrderListView(ListView):
    queryset = Order.objects.all()
    context_object_name = 'orders'
    paginate_by = 5

class SearchOrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    paginate_by = 5
    template_name = 'invoices/order_list.html'

    def get_queryset(self):
        query = self.request.REQUEST.get("q")
        return self.model.objects.filter(Q(customer__surname__contains=query)| Q(customer__name__contains=query))

class InvoiceListView(ListView):
    queryset = Invoice.objects.all()
    context_object_name = 'invoices'
    paginate_by = 5

class SearchInvoiceListView(ListView):
    model = Invoice
    context_object_name = 'invoices'
    paginate_by = 5
    template_name = 'invoices/invoice_list.html'

    def get_queryset(self):
        query = self.request.REQUEST.get("q")
        return self.model.objects.filter(Q(customer__surname__contains=query)| Q(customer__name__contains=query))

class PaymentListView(ListView):
    queryset = Payment.objects.all()
    context_object_name = 'payments'
    paginate_by = 8

class PaymentDetailView(DetailView):
    model = Payment
    context_object_name = 'payment'

class PaymentCreateView(CreateView):
    form_class = PaymentForm
    template_name = 'invoices/payment_create_form.html'
    success_url = '/invoices/payments/'

    def form_valid(self, form):
        self.payment = form.save(commit=False)
        self.payment.record_by = self.request.user.get_profile()
        self.payment.lastchange_by = self.request.user.get_profile()
        self.payment.lastchange = datetime.utcnow().replace(tzinfo=utc)
        return super(PaymentCreateView, self).form_valid(form)

class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'invoices/payment_update_form.html'
    success_url = '/invoices/payments/'
    context_object_name = 'payment'

    def form_valid(self, form):
        self.payment = form.save(commit=False)
        self.payment.lastchange_by = self.request.user.get_profile()
        self.payment.lastchange = datetime.utcnow().replace(tzinfo=utc)
        return super(PaymentUpdateView, self).form_valid(form)

class PaymentDeleteView(DeleteView):
    model = Payment
    form_class = PaymentForm
    success_url = '/invoices/payments'
    context_object_name = 'payment'

class InvoiceDetailView(DetailView):
    model = Invoice
    context_object_name = 'invoice'

class InvoicePrintView(DetailView): # Temporary view
    model = Invoice
    context_object_name = 'invoice'
    template_name = 'invoices/invoice_detail.html'

class InvoicePrintView(SingleObjectMixin, View):
    """ This view invoices generate a pdf"""
    model = Invoice

    def get(self, request, *args, **kwargs):
        invoice = self.get_object()
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=\"%s-%s\"" % (invoice.id, invoice.date.year)
        draw_pdf(response, invoice)
        return response

class OrderDetailView(DetailView):
    model = Order
    context_object_name = 'order'

class OrderCreateView(CreateView):
    form_class = OrderForm
    template_name = 'invoices/order_create_form.html'
    success_url = '/invoices/orders/'

    def form_valid(self, form):
        self.order = form.save(commit=False)
        self.order.record_by = self.request.user.get_profile()
        self.order.lastchange_by = self.request.user.get_profile()
        self.order.lastchange = datetime.utcnow().replace(tzinfo=utc)
        return super(OrderCreateView, self).form_valid(form)

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'invoices/order_update_form.html'
    success_url = '/invoices/orders/'
    context_object_name = 'order'

    def form_valid(self, form):
        self.order = form.save(commit=False)
        self.order.lastchange_by = self.request.user.get_profile()
        self.order.lastchange = datetime.utcnow().replace(tzinfo=utc)
        self.success_url = reverse('order-detail', args=[self.kwargs['pk']])
        return super(OrderUpdateView, self).form_valid(form)

class OrderDeleteView(DeleteView):
    model = Order
    form_class = OrderForm
    success_url = '/invoices/orders'
    context_object_name = 'order'

class ItemCreateView(CreateView):
    form_class = ItemForm
    template_name = 'invoices/item_create_form.html'
    success_url = '/invoices/items/'

    def get_form_class(self):
        """Show in price select only the prices from the catalog choosen in the order"""
        form = super(ItemCreateView, self).get_form_class()
        order = get_object_or_404(Order, id=self.kwargs['order'])
        form.base_fields['price'].queryset = order.catalog.price_set
        return form

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, id=self.kwargs['order'])
        return context

    def form_valid(self, form):
        self.item = form.save(commit=False)
        self.item.price.product.sell(self.item.pieces)
        self.item.order = get_object_or_404(Order, id=self.kwargs['order'])
        self.item.order.lastchange_by = self.request.user.get_profile()
        self.item.order.lastchange = datetime.utcnow().replace(tzinfo=utc)
        self.item.order.save() # If an item is added to an order update last change author and last change datetime for that order
        self.success_url = reverse('order-detail', args=[self.kwargs['order']])
        return super(ItemCreateView, self).form_valid(form)

    def get_initial(self):
        self.initial = super(ItemCreateView, self).get_initial()
        self.initial['pieces'] = 1
        return self.initial

class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'invoices/item_update_form.html'
    success_url = '/invoices/items/'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, id=self.kwargs['order'])
        return context

    def form_valid(self, form):
        self.item = form.save(commit=False)
        previous_item = get_object_or_404(Item, id=self.item.id)
        difference = previous_item.pieces - self.item.pieces
        self.item.price.product.release(difference)
        self.item.order = get_object_or_404(Order, id=self.kwargs['order'])
        self.item.order.lastchange_by = self.request.user.get_profile()
        self.item.order.lastchange = datetime.utcnow().replace(tzinfo=utc)
        self.item.order.save() # If an item in an order is changed update last change author and last change datetime for that order
        self.success_url = reverse('order-detail', args=[self.kwargs['order']])
        return super(ItemUpdateView, self).form_valid(form)

class ItemDeleteView(DeleteView):
    model = Item
    form_class = ItemForm
    success_url = '/invoices/items'
    context_object_name = 'item'

    def get_success_url(self):
        self.success_url = reverse('order-detail', args=[self.kwargs['order']])
        return self.success_url

# class OrderInvoiceView(SingleObjectMixin, SingleObjectTemplateResponseMixin, View):
#     """ This view invoices an order creating a Invoice object and deleting the existing order"""
#     model = Order
#     template_name = 'invoices/order_invoice.html'
#     context_object_name = 'order'

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated():
#             return HttpResponseForbidden()
#         order = self.get_object()
#         order.invoiced = True # in pre_delete_item avoid to release items for an invoiced order
#         order.lastchange_by = request.user.get_profile()
#         order.save()

#         invoice = Invoice.objects.create(customer=order.customer, issuer=request.user.get_profile())
#         for item in order.item_set.all():
#             print item
#             voice = Voice.objects.create(invoice=invoice, description=item.__unicode__(),
#                                          pieces=item.pieces, unit_price=item.price.price_out,
#                                          amount=item.amount, vat=item.price.vat_out,
#                                          amount_novat=item.amount_novat, unit_price_novat=item.price.unit_price)
#             voice.save()

#         order.delete()

#         return HttpResponseRedirect(reverse('invoices'))

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return self.render_to_response(self.get_context_data())

class InvoiceCreateView(CreateView):
    """ This view invoices an order creating a Invoice object and deleting the existing order"""
    form_class = InvoiceForm
    template_name = 'invoices/invoice_create_form.html'
    success_url = '/invoices/invoices/'

    def form_valid(self, form):
        self.invoice = form.save(commit=False)
        order = get_object_or_404(Order, id=self.kwargs['order'])
        order.invoiced = True # in pre_delete_item avoid to release items for an invoiced order
        order.lastchange_by = self.request.user.get_profile()
        order.save()
        self.invoice.customer = order.customer
        self.invoice.issuer = self.request.user.get_profile()
        temp_output = super(InvoiceCreateView, self).form_valid(form) # saving self.invoice to have a self.invoce.id needed in voice.create
        for item in order.item_set.all():
            voice = Voice.objects.create(invoice=self.invoice, description=item.__unicode__(),
                                         pieces=item.pieces, unit_price=item.price.price_out,
                                         amount=item.amount, vat=item.price.vat_out,
                                         amount_novat=item.amount_novat, unit_price_novat=item.price.unit_price)
            voice.save()
        order.delete()
        return temp_output

class HeadingListView(ListView):
    queryset = InvoiceHeading.objects.all()
    context_object_name = 'headings'
    paginate_by = 5

class HeadingDetailView(DetailView):
    model = InvoiceHeading
    context_object_name = 'heading'

class HeadingCreateView(CreateView):
    form_class = HeadingForm
    template_name = 'invoices/invoiceheading_create_form.html'
    success_url = '/invoices/headings/'

    def form_valid(self, form):
        self.InvoiceHeading = form.save(commit=False)
        self.InvoiceHeading.record_by = self.request.user.get_profile()
        self.InvoiceHeading.lastchange_by = self.request.user.get_profile()
        self.InvoiceHeading.lastchange = datetime.utcnow().replace(tzinfo=utc)
        return super(HeadingCreateView, self).form_valid(form)

class HeadingUpdateView(UpdateView):
    model = InvoiceHeading
    form_class = HeadingForm
    template_name = 'invoices/invoiceheading_update_form.html'
    success_url = '/invoices/headings/'
    context_object_name = 'heading'

    def form_valid(self, form):
        self.InvoiceHeading = form.save(commit=False)
        self.InvoiceHeading.lastchange_by = self.request.user.get_profile()
        self.InvoiceHeading.lastchange = datetime.utcnow().replace(tzinfo=utc)
        self.success_url = reverse('heading-detail', args=[self.kwargs['pk']])
        return super(HeadingUpdateView, self).form_valid(form)

class HeadingDeleteView(DeleteView):
    model = InvoiceHeading
    form_class = HeadingForm
    success_url = '/invoices/headings'
    context_object_name = 'heading'
