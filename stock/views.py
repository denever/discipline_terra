# Create your views here.
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from datetime import datetime
from django.utils.timezone import utc

from stock.models import *

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from stock.forms import ProductForm, PackageForm, CategoryForm

class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class WarningProductListView(ListView):
     context_object_name = 'products'
     paginate_by = 5
     template_name = 'stock/product_warning_list.html'

     def get_queryset(self):
         filtered = [x for x in Product.objects.all() if x.status =='warning']
         return filtered

     def get_context_data(self, **kwargs):
        context = super(WarningProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class DangerProductListView(ListView):
     context_object_name = 'products'
     paginate_by = 5
     template_name = 'stock/product_danger_list.html'

     def get_queryset(self):
         filtered = [x for x in Product.objects.all() if x.status == 'danger']
         return filtered

     def get_context_data(self, **kwargs):
        context = super(DangerProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class SearchProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 5
    template_name = 'stock/product_list.html'

    def get_queryset(self):
        query = self.request.REQUEST.get("q")
        return self.model.objects.filter(description__icontains=query)

    def get_context_data(self, **kwargs):
        context = super(SearchProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductByCategoryListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 5
    template_name = 'stock/product_category_list.html'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['pk'])
        return category.product_set.all()

    def get_context_data(self, **kwargs):
        context = super(ProductByCategoryListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['active_cat_id'] = self.kwargs['pk']
        return context

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
        self.product.lastchange_by = self.request.user.get_profile()
        self.product.lastchange = datetime.utcnow().replace(tzinfo=utc)
        return super(ProductCreateView, self).form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'stock/product_update_form.html'
    success_url = '/stock/products/'
    context_object_name = 'product'

    def form_valid(self, form):
        self.product = form.save(commit=False)
        self.product.lastchange_by = self.request.user.get_profile()
        self.product.lastchange = datetime.utcnow().replace(tzinfo=utc)
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
        self.package.lastchange_by = self.request.user.get_profile()
        self.package.lastchange = datetime.utcnow().replace(tzinfo=utc)
        return super(PackageCreateView, self).form_valid(form)

class PackageUpdateView(UpdateView):
    model = Package
    form_class = PackageForm
    template_name = 'stock/package_update_form.html'
    success_url = '/stock/packages/'
    context_object_name = 'package'

    def form_valid(self, form):
        self.package = form.save(commit=False)
        self.package.lastchange_by = self.request.user.get_profile()
        self.package.lastchange = datetime.utcnow().replace(tzinfo=utc)
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


class CategoryCreateView(CreateView):
    form_class = CategoryForm
    template_name = 'stock/category_create_form.html'
    success_url = '/stock/products/'

    def form_valid(self, form):
        self.category = form.save(commit=False)
        self.category.record_by = self.request.user.get_profile()
        self.category.lastchange_by = self.request.user.get_profile()
        self.category.lastchange = datetime.utcnow().replace(tzinfo=utc)
        return super(CategoryCreateView, self).form_valid(form)

class CategoryDeleteView(DeleteView):
    model = Category
    form_class = CategoryForm
    success_url = '/stock/products'
    context_object_name = 'category'
