from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from invoices.models import *

# Create your views here.

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from invoices.forms import CustomerForm, OrderForm, ItemForm

class CustomerListView(ListView):
    queryset = Customer.objects.all()
    context_object_name = 'customers'
    paginate_by = 5

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
        self.customer.lastupdate_by = self.request.user.get_profile()
        return super(CustomerCreateView, self).form_valid(form)

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'invoices/customer_update_form.html'
    success_url = '/invoices/customers/'
    context_object_name = 'customer'

    def form_valid(self, form):
        self.customer = form.save(commit=False)
        self.customer.lastupdate_by = self.request.user.get_profile()
        self.customer.newrevision_needed = True
        self.success_url = reverse('customer-detail', args=[self.kwargs['pk']])
        return super(CustomerUpdateView, self).form_valid(form)

    # def get_initial(self):
    #     self.initial = super(CustomerUpdateView, self).get_initial()
    #     self.initial['ateco_sector'] = self.object.ateco_sector.name
    #     self.initial['cpi'] = self.object.cpi.name
    #     return self.initial

class CustomerDeleteView(DeleteView):
    model = Customer
    form_class = CustomerForm
    success_url = '/invoices/customers'
    context_object_name = 'customer'


class OrderListView(ListView):
    queryset = Order.objects.all()
    context_object_name = 'orders'
    paginate_by = 5

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
        self.order.lastupdate_by = self.request.user.get_profile()
        return super(OrderCreateView, self).form_valid(form)

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'invoices/order_update_form.html'
    success_url = '/invoices/orders/'
    context_object_name = 'order'

    def form_valid(self, form):
        self.order = form.save(commit=False)
        self.order.lastupdate_by = self.request.user.get_profile()
        self.order.newrevision_needed = True
        self.success_url = reverse('order-detail', args=[self.kwargs['pk']])
        return super(OrderUpdateView, self).form_valid(form)

    # def get_initial(self):
    #     self.initial = super(OrderUpdateView, self).get_initial()
    #     self.initial['ateco_sector'] = self.object.ateco_sector.name
    #     self.initial['cpi'] = self.object.cpi.name
    #     return self.initial

class OrderDeleteView(DeleteView):
    model = Order
    form_class = OrderForm
    success_url = '/invoices/orders'
    context_object_name = 'order'

class ItemCreateView(CreateView):
    form_class = ItemForm
    template_name = 'invoices/item_create_form.html'
    success_url = '/invoices/items/'

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, id=self.kwargs['order'])
        return context

    def form_valid(self, form):
        self.item = form.save(commit=False)
        self.item.order = get_object_or_404(Order, id=self.kwargs['order'])
        self.item.record_by = self.request.user.get_profile()
        self.item.lastupdate_by = self.request.user.get_profile()
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

    def form_valid(self, form):
        self.item = form.save(commit=False)
        self.item.lastupdate_by = self.request.user.get_profile()
        self.item.order = get_object_or_404(Order, id=self.kwargs['order'])
        self.success_url = reverse('order-detail', args=[self.kwargs['order']])
        return super(ItemUpdateView, self).form_valid(form)

    # def get_initial(self):
    #     self.initial = super(ItemUpdateView, self).get_initial()
    #     self.initial['ateco_sector'] = self.object.ateco_sector.name
    #     self.initial['cpi'] = self.object.cpi.name
    #     return self.initial

class ItemDeleteView(DeleteView):
    model = Item
    form_class = ItemForm
    success_url = '/invoices/items'
    context_object_name = 'item'
