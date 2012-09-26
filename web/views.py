
from django.http import HttpResponse
from django.template import Context, RequestContext, loader
from web.models import TaxonomyArea, TaxonomyCategory, TaxonomyItem, Reference
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
import os
from django.conf import settings
from reference_parse import reference_entries, html_format

os.environ['DJANGO_SETTINGS_MODULE'] = "viscommunityweb.settings"
email_prefix = "[OXVIS] "
email_to = "simon.walton@oerc.ox.ac.uk"

def index(request):
	t = loader.get_template("templates/index.html")
	return HttpResponse(t.render(Context()))

def taxonomy(request):
	t = loader.get_template("templates/taxonomy.html")
	taxonomies = TaxonomyCategory.objects.all()
	c = Context({ 'taxonomies' : taxonomies, })
	return HttpResponse(t.render(c))

def taxonomy_detail(request, taxonomy_id):
	taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)
	html = html_format(taxonomy.detail_html)
	if len(html) == 0:
		html = "There is currently no information on this taxonomy item."

	return render_to_response("templates/taxonomy_detail.html",
		 {'taxonomy': taxonomy,
		 'formatted_detail': html,
		 'references': reference_entries(taxonomy.detail_html) })

def request_ownership(request, taxonomy_id):
	taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)
	return render_to_response("templates/contact.html", {'taxonomy': taxonomy},  context_instance=RequestContext(request))

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
			settings.ADMINS[0][1] + " to resolve."}) 
	else:
		return render_to_response("templates/contact.html", {'success_message':'Your request was sent successfully!'})

def references(request):
	refs = Reference.objects.all()
	return render_to_response("templates/references.html", {'references': refs })
