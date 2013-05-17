"""
 Views - see urls.py for the mappings from URLs to the defs here.
"""

from django.http import HttpResponse
from django.template import Context, RequestContext, loader
from web.models import TaxonomyArea, TaxonomyCategory, TaxonomyItem, Reference
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
import os
from django.conf import settings
from reference_parse import reference_entries, html_format
from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout, login as django_login
import taxonomy_backend, reference_backend
import json

# couple of globals
os.environ['DJANGO_SETTINGS_MODULE'] = "viscommunityweb.settings"
email_prefix = "[OXVIS] "
email_to = "simon.walton@oerc.ox.ac.uk"

# index page
def index(request):
    recent_items = TaxonomyItem.objects.exclude(detail_html="").order_by('last_updated')[:3]
    return render_to_response("templates/index.html", {'recent_taxonomy_items': recent_items},
                              context_instance=RequestContext(request))

# taxonomy list
def taxonomy(request):
    taxonomies = TaxonomyCategory.objects.all()
    return render_to_response("templates/taxonomy.html", {'taxonomies': taxonomies},
                              context_instance=RequestContext(request))


def taxonomy_alpha(request):
    index = taxonomy_backend.alphabetic_index()
    return render_to_response("templates/taxonomy-alpha.html", {'index': index},
                              context_instance=RequestContext(request))

# taxonomy detail page
def taxonomy_detail(request, taxonomy_id):
    taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)
    html = html_format(taxonomy.detail_html)

    if len(html) == 0:
        html = "There is currently no information on this taxonomy item."

    refer = reference_backend.sorted_reference_list(request, reference_entries(taxonomy.detail_html))
    bibtex_texts = json.dumps([x.bibtex for x in refer])

    print "Got %i refs" % len(refer)

    return render_to_response("templates/taxonomy_detail.html",
                              {'taxonomy': taxonomy, 'formatted_detail': html, 'references': refer,
                               'bibtex_texts': bibtex_texts}, context_instance=RequestContext(request))

# contact page for ownership request
def request_ownership(request, taxonomy_id):
    taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)
    return render_to_response("templates/contact.html", {'taxonomy': taxonomy},
                              context_instance=RequestContext(request))

# general contact page
def contact(request):
    return render_to_response("templates/contact.html", context_instance=RequestContext(request))

# accessed through a POST to send email to the admins regarding above
def request_ownership_send(request):
    email_subject = email_prefix + "Request for taxonomy ownership"
    email_from = request.POST['email']
    email_name = request.POST['name']
    email_body = request.POST['comments']

    try:
        send_mail(email_subject, email_body, email_from,
                  [item[1] for item in settings.ADMINS], fail_silently=False)
    except:
        return render_to_response("templates/contact.html",
                                  {
                                  'error_message': "There was a problem sending the email. Please ensure all fields are filled in correctly. Please contact " +
                                                   settings.ADMINS[0][1] + " if the problem continues."},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response("templates/contact.html", {'success_message': 'Your request was sent successfully!'},
                                  context_instance=RequestContext(request))

# big list of all references in database (future: sorting/filtering etc)
def references(request):
    refs = reference_backend.sorted_reference_list(request)

    return render_to_response("templates/references.html",
                              {'references': refs, 'bibtex_texts': json.dumps([x.bibtex for x in refs])},
                              context_instance=RequestContext(request))

# search
def search(request):
    searchTerm = request.GET['q']
    references = Reference.objects.all()

    searchResult = [];

    for reference in references:
        if searchTerm in reference.bibtex:
            searchResult.append(reference)

    return render_to_response("templates/search.html",
                              {"searchTerm": searchTerm, "size": len(searchResult), "searchResults": searchResult},
                              context_instance=RequestContext(request))


def account(request):
    items_owned = TaxonomyItem.objects.filter(
        owners__id__contains=request.user.id) if request.user.id is not None else None
    return render_to_response("templates/account.html", {'items_owned': items_owned},
                              context_instance=RequestContext(request))


def profile(request):
    return render_to_response("templates/profile.html", {},
                              context_instance=RequestContext(request))