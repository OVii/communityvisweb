from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'viscommunityweb.views.home', name='home'),
                       # url(r'^viscommunityweb/', include('viscommunityweb.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^accounts/', include('registration.backends.default.urls')),
                       url(r'^profiles/', include('profiles.urls')),
                       url(r'^$', 'web.views.index'),
                       url(r'^accounts/profile', 'web.views.profile'),
                       url(r'^taxonomy/$', 'web.views.taxonomy'),
                       url(r'^taxonomy_alpha/$', 'web.views.taxonomy_alpha'),
                       url(r'^taxonomy/(?P<taxonomy_id>\d+)/$', 'web.views.taxonomy_detail'),
                       url(r'^request_ownership/(?P<taxonomy_id>\d+)/$', 'web.views.request_ownership'),
                       url(r'^request_ownership/send/$', 'web.views.request_ownership_send'),
                       url(r'^contact/$', 'web.views.contact'),
                       url(r'^references/$', 'web.views.references'),
                       url(r'^search/$', 'web.views.search'),
                       url(r'^account/$', 'web.views.account'),
                       url(r'^orcid$', 'web.views.orcid_profile'),

                       #url(r'^web/references/(?P<reference_id>\d+)/$', 'web.views.reference_detail')

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)
