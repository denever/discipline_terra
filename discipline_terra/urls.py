from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'discipline_terra.views.home', name='home'),
    # url(r'^discipline_terra/', include('discipline_terra.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
                       url(r'^$', include('cover.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^stock/', include('stock.urls')),
                       url(r'^catalog/', include('catalog.urls')),
                       url(r'^invoices/', include('invoices.urls')),
                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^customers/', include('customers.urls')),
)
