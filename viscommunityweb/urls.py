from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'viscommunityweb.views.home', name='home'),
                       # url(r'^viscommunityweb/', include('viscommunityweb.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


                       url(r'^accounts/', include('registration.backends.default.urls')),
                       url(r'^profiles/', include('profiles.urls'), name='profiles'),

                       url(r'^$', 'web.views.index', name='community-home'),
                       url(r'^accounts/profile', 'web.views.profile', name='profile'),
                       url(r'^profile/(\w+)', 'web.views.public_profile', name='pub_profile'),


                       url(r'^taxonomy/add/$', 'web.views.taxonomy_add', name='add_taxonomy'),
                       url(r'^taxonomy/edit/(?P<taxonomy_id>\d+)/$', 'web.views.taxonomy_edit', name='edit_taxonomy'),

                       url(r'^taxonomy/add/action/$', 'web.views.taxonomy_add_action', name='add_taxonomy_action'),
                       url(r'^taxonomy/edit/action/$', 'web.views.taxonomy_edit_action', name='edit_taxonomy_action'),

                       url(r'^reference/edit/(?P<reference_id>\d+)/$', 'web.views.reference_edit', name='edit_reference'),
                       url(r'^reference/add/manual$', 'web.views.reference_add_manual', name='add_reference'),
                       url(r'^reference/add/file$', 'web.views.reference_add_upload_file', name='upload_bibtex'),
                       url(r'^reference/add/text$', 'web.views.reference_add_upload_text', name='upload_bibtex_text'),

                       url(r'^reference/remove/(?P<taxonomy_id>\d+)/(?P<reference_id>\d+)/$',
                           'web.views.reference_remove', name='remove_reference'),
                       url(r'^reference/(?P<reference_id>\d+)/$', 'web.views.reference_detail',
                           name='reference_detail'),

                       url(r'^taxonomy/$', 'web.views.taxonomy', name='taxonomy'),
                       url(r'^taxonomy_alpha/$', 'web.views.taxonomy_alpha', name='taxonomy_alpha'),
                       url(r'^taxonomy/(?P<taxonomy_id>\d+)/$', 'web.views.taxonomy_detail', name='taxonomy_detail'),
                       url(r'^taxonomy/download/(\d+)/$', 'web.views.taxonomy_download', name='taxonomy_download'),

                       url(r'^request_ownership/(?P<taxonomy_id>\d+)$', 'web.views.request_ownership_send',
                           name='request_ownership'),
                       url(r'^request_ownership/response/(?P<approval_id>\d+)$', 'web.views.request_ownership_response',
                           name='request_ownership_response'),
                       url(r'^revoke_ownership/(?P<taxonomy_id>\d+)$', 'web.views.revoke_ownership',
                           name='revoke_ownership'),

                       url(r'^enquiry/(?P<taxonomy_id>\d+)/$', 'web.views.handleTaxonomyEnquiry', name='enquiry'),
                       url(r'^enquiry/(?P<taxonomy_id>\d+)/(?P<reference_id>\d+)/$', 'web.views.handleReferenceEnquiry',
                           name='enquiry_reference'),
                       url(r'^enquiry/(?P<decision>\w+)/(?P<enquiry_id>\d+)/$', 'web.views.respondToTaxonomyEnquiry',
                           name='enquiry_decision'),

                       url(r'^contact/$', 'web.views.contact', name='contact'),
                       url(r'^contact/send', 'web.views.contact_send', name='contact_send'),

                       url(r'^search/$', 'web.views.search', name='search'),
                       url(r'^account/$', 'web.views.account', name='account'),
                       url(r'^orcid$', 'web.views.orcid_profile', name='orcid'),

                       url(r'^volunteer$', 'web.views.volunteer', name='volunteer'),

                       url(r'^admin/', include(admin.site.urls), name='admin'),

)
