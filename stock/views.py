# Create your views here.
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from stock.models import *

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from stock.forms import ProductForm, PackageForm

class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 5

class WarningProductListView(ListView):
     context_object_name = 'products'
     paginate_by = 5
     template_name = 'stock/product_list.html'

     def get_queryset(self):
         filtered = [x for x in Product.objects.all() if x.status =='warning']
         return filtered

class DangerProductListView(ListView):
     context_object_name = 'products'
     paginate_by = 5
     template_name = 'stock/product_list.html'

     def get_queryset(self):
         filtered = [x for x in Product.objects.all() if x.status == 'danger']
         return filtered

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = 'stock/product_create_form.html'
    success_url = '/stock/products/'

    def form_valid(self, form):
        self.product = form.save(commit=False)
        self.product.record_by = self.request.user.get_profile()
        self.product.lastupdate_by = self.request.user.get_profile()
        return super(ProductCreateView, self).form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'stock/product_update_form.html'
    success_url = '/stock/products/'
    context_object_name = 'product'

    def form_valid(self, form):
        self.product = form.save(commit=False)
        self.product.lastupdate_by = self.request.user.get_profile()
        self.product.newrevision_needed = True
        self.success_url = reverse('product-detail', args=[self.kwargs['pk']])
        return super(ProductUpdateView, self).form_valid(form)

    # def get_initial(self):
    #     self.initial = super(ProductUpdateView, self).get_initial()
    #     self.initial['ateco_sector'] = self.object.ateco_sector.name
    #     self.initial['cpi'] = self.object.cpi.name
    #     return self.initial

class ProductDeleteView(DeleteView):
    model = Product
    form_class = ProductForm
    success_url = '/stock/products'
    context_object_name = 'product'

# Packages managment

class PackageListView(ListView):
    queryset = Package.objects.all()
    context_object_name = 'packages'
    paginate_by = 5

class PackageDetailView(DetailView):
    model = Package
    context_object_name = 'package'

class PackageCreateView(CreateView):
    form_class = PackageForm
    template_name = 'stock/package_create_form.html'
    success_url = '/stock/packages/'

    def form_valid(self, form):
        self.package = form.save(commit=False)
        self.package.record_by = self.request.user.get_profile()
        self.package.lastupdate_by = self.request.user.get_profile()
        return super(PackageCreateView, self).form_valid(form)

class PackageUpdateView(UpdateView):
    model = Package
    form_class = PackageForm
    template_name = 'stock/package_update_form.html'
    success_url = '/stock/packages/'
    context_object_name = 'package'

    def form_valid(self, form):
        self.package = form.save(commit=False)
        self.package.lastupdate_by = self.request.user.get_profile()
        self.package.newrevision_needed = True
        self.success_url = reverse('package-detail', args=[self.kwargs['pk']])
        return super(PackageUpdateView, self).form_valid(form)

    # def get_initial(self):
    #     self.initial = super(PackageUpdateView, self).get_initial()
    #     self.initial['ateco_sector'] = self.object.ateco_sector.name
    #     self.initial['cpi'] = self.object.cpi.name
    #     return self.initial

class PackageDeleteView(DeleteView):
    model = Package
    form_class = PackageForm
    success_url = '/stock/packages/'
    context_object_name = 'package'
