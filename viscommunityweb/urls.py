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

                       url(r'^accounts/', include('registration.backends.default.urls'), name='accounts'),
                       url(r'^profiles/', include('profiles.urls'), name='profiles'),
                       url(r'^$', 'web.views.index', name='index'),
                       url(r'^accounts/profile', 'web.views.profile', name='profile'),
                       url(r'^accounts/logout', 'web.views.logout', name='logout'),
                       url(r'^accounts/login', 'web.views.login', name='login'),

                       url(r'^taxonomy/$', 'web.views.taxonomy', name='taxonomy'),
                       url(r'^taxonomy_alpha/$', 'web.views.taxonomy_alpha', name='taxonomy_alpha'),
                       url(r'^taxonomy/(?P<taxonomy_id>\d+)/$', 'web.views.taxonomy_detail', name='taxonomy_detail'),
                       url(r'^taxonomy/(?P<taxonomy_id>\d+)/download$', 'web.views.taxonomy_download', name='taxonomy_download'),
                       url(r'^request_ownership/(?P<taxonomy_id>\d+)$', 'web.views.request_ownership_send', name='request_ownership'),
                       url(r'^request_ownership/response/(?P<approval_id>\d+)$', 'web.views.request_ownership_response', name='request_ownership_response'),
                       url(r'^revoke_ownership/(?P<taxonomy_id>\d+)$', 'web.views.revoke_ownership', name='revoke_ownership'),

                       url(r'^enquiry/(?P<taxonomy_id>\d+)/$', 'web.views.handleTaxonomyEnquiry', name='enquiry'),
                       url(r'^enquiry/(?P<taxonomy_id>\d+)/(?P<reference_id>\d+)/$', 'web.views.handleReferenceEnquiry', name='enquiry'),
                       url(r'^enquiry/(?P<decision>\w+)/(?P<enquiry_id>\d+)/$', 'web.views.respondToTaxonomyEnquiry', name='enquiry'),

                       url(r'^contact/$', 'web.views.contact', name='contact'),
                       url(r'^references/$', 'web.views.references', name='references'),
                       url(r'^search/$', 'web.views.search', name='search'),
                       url(r'^account/$', 'web.views.account', name='account'),
                       url(r'^orcid$', 'web.views.orcid_profile', name='orcid'),

                       #url(r'^web/references/(?P<reference_id>\d+)/$', 'web.views.reference_detail')

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)
