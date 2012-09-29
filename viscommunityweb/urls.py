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

	url(r'^web/$', 'web.views.index'),
	url(r'^web/taxonomy/$', 'web.views.taxonomy'),
	url(r'^web/taxonomy/(?P<taxonomy_id>\d+)/$', 'web.views.taxonomy_detail'),
	url(r'^web/request_ownership/(?P<taxonomy_id>\d+)/$', 'web.views.request_ownership'),
	url(r'^web/request_ownership/send/$', 'web.views.request_ownership_send'),
	url(r'^web/references/$', 'web.views.references'),
    url(r'^web/register/$', 'web.views.register'),
    url(r'^web/sign_in/$', 'web.views.sign_in'),
    url(r'^web/do_login/$', 'web.views.login'),
	url(r'^web/do_logout/$', 'web.views.logout'),
	#url(r'^web/references/(?P<reference_id>\d+)/$', 'web.views.reference_detail')

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
