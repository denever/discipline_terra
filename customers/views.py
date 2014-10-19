from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.timezone import utc

from customers.models import *
from customers.forms import CustomerForm

from datetime import datetime
# Create your views here.
from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Create your views here.
class CustomerListView(ListView):
    queryset = Customer.objects.all()
    context_object_name = 'customers'
    paginate_by = 5

class SearchCustomerListView(ListView):
    model = Customer
    context_object_name = 'customers'
    paginate_by = 5
    template_name = 'customers/customer_list.html'

    def get_queryset(self):
        query = self.request.REQUEST.get("q")
        return self.model.objects.filter(Q(surname__contains=query)| Q(name__contains=query))

class CustomerDetailView(DetailView):
    model = Customer
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    form_class = CustomerForm
    template_name = 'customers/customer_create_form.html'
    success_url = '/customers/customers/'

    def form_valid(self, form):
        self.customer = form.save(commit=False)
        self.customer.record_by = self.request.user.profile
        self.customer.lastchange_by = self.request.user.profile
        self.customer.lastchange = datetime.utcnow().replace(tzinfo=utc)
        return super(CustomerCreateView, self).form_valid(form)

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_update_form.html'
    success_url = '/customers/customers/'
    context_object_name = 'customer'

    def form_valid(self, form):
        self.customer = form.save(commit=False)
        self.customer.lastchange_by = self.request.user.profile
        self.customer.lastchange = datetime.utcnow().replace(tzinfo=utc)
        self.success_url = reverse('customer-detail', args=[self.kwargs['pk']])
        return super(CustomerUpdateView, self).form_valid(form)

class CustomerDeleteView(DeleteView):
    model = Customer
    form_class = CustomerForm
    success_url = '/customers/customers'
    context_object_name = 'customer'
