
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

# couple of globals
os.environ['DJANGO_SETTINGS_MODULE'] = "viscommunityweb.settings"
email_prefix = "[OXVIS] "
email_to = "simon.walton@oerc.ox.ac.uk"

# index page
def index(request):
	t = loader.get_template("templates/index.html")
	return HttpResponse(t.render(RequestContext(request)))

# sign in page.
def sign_in(request):
    t = loader.get_template("templates/signin.html")
    return HttpResponse(t.render(RequestContext(request)))

# register page.
def register(request):
    t = loader.get_template("templates/register.html")
    return HttpResponse(t.render(RequestContext(request)))

# taxonomy list
def taxonomy(request):
	taxonomies = TaxonomyCategory.objects.all()
	return render_to_response("templates/taxonomy.html", {'taxonomies': taxonomies}, context_instance=RequestContext(request))

# taxonomy detail page
def taxonomy_detail(request, taxonomy_id):
	taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)
	html = html_format(taxonomy.detail_html)
	if len(html) == 0:
		html = "There is currently no information on this taxonomy item."

	return render_to_response("templates/taxonomy_detail.html",
		 {'taxonomy': taxonomy,
		 'formatted_detail': html,
		 'references': reference_entries(taxonomy.detail_html) },
		 context_instance=RequestContext(request))

# contact page for ownership request
def request_ownership(request, taxonomy_id):
	taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)
	return render_to_response("templates/contact.html", {'taxonomy': taxonomy},  context_instance=RequestContext(request))

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
		return render_to_response("templates/contact.html", {'error_message':"There was a problem sending the email. Please contact " + 
			settings.ADMINS[0][1] + " to resolve."},
			context_instance=RequestContext(request)) 
	else:
		return render_to_response("templates/contact.html", {'success_message':'Your request was sent successfully!'},
			 context_instance=RequestContext(request))

# big list of all references in database (future: sorting/filtering etc)
def references(request):
	refs = Reference.objects.all()
	return render_to_response("templates/references.html", {'references': refs }, context_instance=RequestContext(request))

# login POST
def login(request):
	user = authenticate(username=request.POST['username'], password=request.POST['password'])
	if user is not None:
		django_login(request,user)
	return render_to_response("templates/index.html", context_instance=RequestContext(request))	
	
# logout POST
def logout(request):
	django_logout(request)
	return render_to_response("templates/index.html", context_instance=RequestContext(request))	
