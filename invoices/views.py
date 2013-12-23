from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from invoices.models import *

# Create your views here.

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from invoices.forms import CustomerForm

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
