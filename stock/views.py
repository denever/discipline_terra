# Create your views here.
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from stock.models import *

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = 'stock/product_create_form.html'
    success_url = '/stock/'

    def form_valid(self, form):
        self.product = form.save(commit=False)
        self.product.record_by = self.request.user.get_profile()
        self.product.lastupdate_by = self.request.user.get_profile()
        return super(ProductCreateView, self).form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_update_form.html'
    success_url = '/stock/'
    context_object_name = 'product'

    def form_valid(self, form):
        self.product = form.save(commit=False)
        self.product.lastupdate_by = self.request.user.get_profile()
        self.product.newrevision_needed = True
        self.success_url = reverse('product-detail', args=self.kwargs['pk'])
        return super(ProductUpdateView, self).form_valid(form)

    # def get_initial(self):
    #     self.initial = super(ProductUpdateView, self).get_initial()
    #     self.initial['ateco_sector'] = self.object.ateco_sector.name
    #     self.initial['cpi'] = self.object.cpi.name
    #     return self.initial

class ProductDeleteView(DeleteView):
    model = Product
    form_class = ProductForm
    success_url = '/products/'
    context_object_name = 'product'
