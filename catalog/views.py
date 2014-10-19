from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from datetime import datetime
from django.utils.timezone import utc

from catalog.models import *

# Create your views here.

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from catalog.forms import PriceForm, CatalogForm

class CatalogListView(ListView):
    queryset = Catalog.objects.all()
    context_object_name = 'catalogs'
    paginate_by = 5

class CatalogCreateView(CreateView):
    form_class = CatalogForm
    template_name = 'catalog/catalog_create_form.html'
    success_url = '/catalog/catalogs/'

class CatalogUpdateView(UpdateView):
    model = Catalog
    form_class = CatalogForm
    template_name = 'catalog/catalog_update_form.html'
    success_url = '/catalog/catalogs/'
    context_object_name = 'catalog'

class CatalogDeleteView(DeleteView):
    model = Catalog
    form_class = CatalogForm
    success_url = '/catalog/catalogs'
    context_object_name = 'catalog'

class PriceListView(ListView):
    queryset = Price.objects.all()
    context_object_name = 'prices'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PriceListView, self).get_context_data(**kwargs)
        context['catalogs'] = Catalog.objects.all()
        return context

class SearchPriceListView(ListView):
    model = Price
    context_object_name = 'prices'
    paginate_by = 5
    template_name = 'catalog/price_catalog_list.html'

    def get_queryset(self):
        catalog = get_object_or_404(Catalog, id=self.kwargs['pk'])
        query = self.request.REQUEST.get("q")
        return catalog.price_set.filter(product__description__icontains=query)

    def get_context_data(self, **kwargs):
        context = super(SearchPriceListView, self).get_context_data(**kwargs)
        context['catalogs'] = Catalog.objects.all()
        context['current_catalog'] = get_object_or_404(Catalog, id=self.kwargs['pk'])
        return context

class PriceListByCatalogView(ListView):
    model = Price
    context_object_name = 'prices'
    paginate_by = 5
    template_name = 'catalog/price_catalog_list.html'

    def get_context_data(self, **kwargs):
        context = super(PriceListByCatalogView, self).get_context_data(**kwargs)
        context['catalogs'] = Catalog.objects.all()
        context['current_catalog'] = get_object_or_404(Catalog, id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        catalog = get_object_or_404(Catalog, id=self.kwargs['pk'])
        return catalog.price_set.all()

class PriceDetailView(DetailView):
    model = Price
    context_object_name = 'price'

class PriceCreateView(CreateView):
    form_class = PriceForm
    template_name = 'catalog/price_create_form.html'
    success_url = '/catalog/prices/'

    def get_context_data(self, **kwargs):
        context = super(PriceCreateView, self).get_context_data(**kwargs)
        context['current_catalog'] = get_object_or_404(Catalog, id=self.kwargs['pk'])
        return context

    def get_initial(self):
        self.initial = super(PriceCreateView, self).get_initial()
        self.initial['catalog'] = get_object_or_404(Catalog, id=self.kwargs['pk'])
        return self.initial

    def form_valid(self, form):
        self.price = form.save(commit=False)
        self.price.record_by = self.request.user.profile
        self.price.lastchange_by = self.request.user.profile
        self.price.lastchange = datetime.utcnow().replace(tzinfo=utc)
        self.success_url = reverse('prices-catalog', args=[self.kwargs['pk']])
        return super(PriceCreateView, self).form_valid(form)

class PriceUpdateView(UpdateView):
    model = Price
    form_class = PriceForm
    template_name = 'catalog/price_update_form.html'
    success_url = '/catalog/prices/'
    context_object_name = 'price'

    def form_valid(self, form):
        self.price = form.save(commit=False)
        self.price.lastchange_by = self.request.user.profile
        self.price.lastchange = datetime.utcnow().replace(tzinfo=utc)
        self.success_url = reverse('price-detail', args=[self.kwargs['pk']])
        return super(PriceUpdateView, self).form_valid(form)

class PriceDeleteView(DeleteView):
    model = Price
    form_class = PriceForm
    success_url = '/catalog/prices'
    context_object_name = 'price'
