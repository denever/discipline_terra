from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from catalog.models import *

# Create your views here.

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from catalog.forms import PriceForm

class PriceListView(ListView):
    queryset = Price.objects.all()
    context_object_name = 'prices'
    paginate_by = 5

class PriceDetailView(DetailView):
    model = Price
    context_object_name = 'price'

class PriceCreateView(CreateView):
    form_class = PriceForm
    template_name = 'catalog/price_create_form.html'
    success_url = '/catalog/prices/'

    def form_valid(self, form):
        self.price = form.save(commit=False)
        self.price.record_by = self.request.user.get_profile()
        self.price.lastupdate_by = self.request.user.get_profile()
        return super(PriceCreateView, self).form_valid(form)

class PriceUpdateView(UpdateView):
    model = Price
    form_class = PriceForm
    template_name = 'catalog/price_update_form.html'
    success_url = '/catalog/prices/'
    context_object_name = 'price'

    def form_valid(self, form):
        self.price = form.save(commit=False)
        self.price.lastupdate_by = self.request.user.get_profile()
        self.price.newrevision_needed = True
        self.success_url = reverse('price-detail', args=[self.kwargs['pk']])
        return super(PriceUpdateView, self).form_valid(form)

    # def get_initial(self):
    #     self.initial = super(PriceUpdateView, self).get_initial()
    #     self.initial['ateco_sector'] = self.object.ateco_sector.name
    #     self.initial['cpi'] = self.object.cpi.name
    #     return self.initial

class PriceDeleteView(DeleteView):
    model = Price
    form_class = PriceForm
    success_url = '/catalog/prices'
    context_object_name = 'price'
