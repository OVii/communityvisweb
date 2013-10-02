"""
 Views - see urls.py for the mappings from URLs to the defs here.
"""
from datetime import datetime
import hashlib
import urllib2
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models import Q
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import logging
from django.utils import simplejson
from viscommunityweb.settings import EMAIL_HOST_USER, SITE_ID, URL_PREPENDER
from web.bibtex_utils.import_utils import saveFile, saveTextToFile
from web.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail, EmailMessage
import os
from django.conf import settings
import taxonomy_backend
import json

# couple of globals
from web.reference_import_couch import bibtex_import

os.environ['DJANGO_SETTINGS_MODULE'] = "viscommunityweb.settings"
email_prefix = "[OXVIS] "
email_to = "eamonn.maguire@oerc.ox.ac.uk"

logger = logging.getLogger(__name__)

# index page
def index(request):
	recent_items = TaxonomyItem.objects.order_by('-last_updated')[:3]
	recent_reference_items = recent_references.get_references()
	return render_to_response("templates/index.html",
							  {'recent_taxonomy_items': recent_items, 'recent_reference_items': recent_reference_items},
							  context_instance=RequestContext(request))


# taxonomy list
def taxonomy(request):
	message = request.GET.get('message', '')
	success = request.GET.get('success', True)
	ajax_url_prefix = settings.AJAX_URL_PREFIX

	taxonomies = TaxonomyCategory.objects.all()
	return render_to_response("templates/taxonomy.html",
			{'taxonomies': taxonomies, 'message': message, 'success': success,'ajax_url_prefix' :ajax_url_prefix},
							  context_instance=RequestContext(request))

def taxonomy_alpha(request):
	index = taxonomy_backend.alphabetic_index()
	return render_to_response("templates/taxonomy-alpha.html", {'index': index},
							  context_instance=RequestContext(request))


# taxonomy detail page
def taxonomy_detail(request, taxonomy_id):
	taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)
	sort_order = request.GET.get('sort')
	references = taxonomy.references(sort_order)

	refer = references

	ownershipRequested = False
	if request.user.is_authenticated():
		existingOwnershipRequestQuery = OwnershipRequest.objects.filter(requester=request.user).filter(
			taxonomyItem=taxonomy)
		if len(existingOwnershipRequestQuery) > 0:
			ownershipRequested = True
	ownerLoggedIn = False
	if request.user in taxonomy.owners.all():
		ownerLoggedIn = True

	return render_to_response("templates/taxonomy_detail.html",
							  {'taxonomy': taxonomy, 'owners': len(taxonomy.owners.all()),
							   'ownerLoggedIn': ownerLoggedIn, 'ownershipRequested': ownershipRequested,
							   'references': refer},
							  context_instance=RequestContext(request))


def taxonomy_download(request, taxonomy_id):
	taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)
	references = taxonomy.references()

	bibtex = ""

	for reference in references:
		bibtex += reference[1]['bibtex'] + "\n"

	response = HttpResponse(bibtex, mimetype='application/text')

	# this is required in Chrome due to problems with spaces and commas in file names
	modifiedTaxonomyName = taxonomy.name.replace(r'\s', '_')
	modifiedTaxonomyName = modifiedTaxonomyName.replace(',', '')

	response['Content-Disposition'] = 'attachment; filename=' + modifiedTaxonomyName + ".bib"
	return response


# general contact page
def contact(request):
	return render_to_response("templates/contact.html", context_instance=RequestContext(request))


# accessed through a POST to send email to the admins regarding above
def request_ownership_send(request, taxonomy_id):
	email_subject = email_prefix + "Request for taxonomy ownership by " + request.user.username
	email_from = request.user.email
	email_body = request.POST['message']

	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)

	ownershipRequest = OwnershipRequest(requester=request.user, taxonomyItem=taxonomyItem, additionalNotes=email_body)
	ownershipRequest.save()

	try:
		send_mail(email_subject, email_body, email_from,
				  [item[1] for item in settings.ADMINS], fail_silently=False)
	except Exception, e:
		return render_to_response("templates/infopage.html",
								  {
								  'messageTitle': 'Problem encountered sending the request.',
								  'messageBody': "There was a problem sending the email. Please ensure all fields "
												 "are filled in correctly. Please contact " +
												 settings.ADMINS[0][1] + " if the problem continues."},
								  context_instance=RequestContext(request))
	else:
		return render_to_response("templates/infopage.html", {
		'messageTitle': 'Request sent successfully!',
		'messageBody': 'Your request was sent successfully! We will get back to you soon!'},
								  context_instance=RequestContext(request))


def request_ownership_response(request, approval_id):
	response = request.POST['type']
	responseDetail = request.POST['responseDetail']
	urlRequestedFrom = request.POST.get('postedFrom', '/')

	print 'Requested from ' + urlRequestedFrom
	ownershipRequest = OwnershipRequest.objects.filter(pk=approval_id).get(pk=approval_id)

	taxonomyItem = ownershipRequest.taxonomyItem
	if response == 'Approved':
		ownershipRequest = OwnershipRequest.objects.filter(pk=approval_id).get(pk=approval_id)
		taxonomyItem = ownershipRequest.taxonomyItem
		taxonomyItem.owners.add(ownershipRequest.requester)
		taxonomyItem.save()

	email_subject = email_prefix + "Request for ownership of " + taxonomyItem.name + " " + response

	email_body_prefix = "We are pleased to welcome you on board Community Vis!\n\n Please login and start managing the references for " + taxonomyItem.name + "!";
	if response != "Approved":
		email_body_prefix = "We are sorry to inform you that we were unable to approve your request. The reason for not doing so is given below.\n\n"

	email_body_reason = responseDetail

	try:
		send_mail(email_subject, email_body_prefix + " " + email_body_reason,
				  EMAIL_HOST_USER,
				  [ownershipRequest.requester.email], fail_silently=False)

	except Exception, e:
		return render_to_response("templates/infopage.html",
								  {
								  'messageTitle': 'Problem encountered sending the message to ' + ownershipRequest.requester.email + '/',
								  'messageBody': "Here are the details\n." + e.message},
								  context_instance=RequestContext(request))
	finally:
		ownershipRequest.delete()

	return HttpResponseRedirect(urlRequestedFrom)


@login_required
def revoke_ownership(request, taxonomy_id):
	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
	taxonomyItem.owners.remove(request.user)

	try:
		email_subject = email_prefix + "Ownership revoked by " + request.user.username + " for " + taxonomyItem.name
		email_from = request.user.email
		email_name = request.user.username
		email_body = email_name + ' has revoked their ownership of ' + taxonomyItem.name
		email_body += request.POST['comments']

		send_mail(email_subject, email_body, email_from,
				  [EMAIL_HOST_USER], fail_silently=False)
	except Exception, e:
		return render_to_response("templates/infopage.html",
								  {
								  'messageTitle': 'Problem encountered sending the request.',
								  'messageBody': "There was a problem sending the email. Please ensure all fields "
												 "are filled in correctly. Please contact " +
												 settings.ADMINS[0][1]
												 + " if the problem continues.\n\nDetailed reason is below: \n\n"
												 + e.message},
								  context_instance=RequestContext(request))
	else:
		return render_to_response("templates/infopage.html",
								  {'messageTitle': 'You have been removed as owner of ' + taxonomyItem.name + '.',
								   'messageBody': "We're sad to see you leave, we hope you come back soon if you get the time!"},
								  context_instance=RequestContext(request))


# big list of all references in database (future: sorting/filtering etc)
""""def references(request):
	pass
	refs = reference_backend.sorted_reference_list(request)

	return render_to_response("templates/references.html",
							  {'references': refs, 'bibtex_texts': json.dumps([x.bibtex for x in refs])},
							  context_instance=RequestContext(request))
"""

# search
def search(request):
	"""    searchOn = request.GET.get('q', '')
	references = Reference.objects.filter(
		Q(title__icontains=searchOn) |
		Q(journal__icontains=searchOn) |
		Q(year__icontains=searchOn) |
		Q(bibtex__icontains=searchOn))
	"""
	result = []#[reference_backend.SortableReference(x) for x in references]
	return render_to_response("templates/search.html",
							  {"searchTerm": searchOn, "size": len(result), "searchResults": result},
							  context_instance=RequestContext(request))


def account(request):
	items_owned = TaxonomyItem.objects.filter(
		owners__id__contains=request.user.id) if request.user.id is not None else None
	return render_to_response("templates/account.html", {'items_owned': items_owned},
							  context_instance=RequestContext(request))


def login(request):
	return render_to_response("registration/login.html", context_instance=RequestContext(request))


def do_logout(request):
	logout(request)
	return render_to_response("registration/logout.html", context_instance=RequestContext(request))


def register(request):
	return render_to_response("registration/registration_form.html", context_instance=RequestContext(request))


def public_profile(request, username):
	userQuery = User.objects.filter(username=username)

	if len(userQuery) > 0:
		requestedUser = userQuery.get(username=username)
		loggedInUser = (requestedUser == request.user)
	else:
		return render_to_response("information.html",
								  {"header": "User does not exist",
								   "message": "No user with the username " + username + " exists."},
								  context_instance=RequestContext(request))

	profile = None

	try:
		if not requestedUser.get_profile() is None:
			profile = requestedUser.get_profile()
	except Exception, e:
		logger.error(str(e.message))
		profile = UserProfile(user=requestedUser)
		profile.save()

	gravatarMD5 = None
	if profile.gravatarEmail:
		gravatarMD5 = hashlib.md5(profile.gravatarEmail).hexdigest()

	taxonomyItems = []

	taxonomyItemsForUser = TaxonomyItem.objects.filter(owners__username=requestedUser.username)
	for userTaxonomyItem in taxonomyItemsForUser:
		taxonomyItems.append(userTaxonomyItem)

	return render_to_response("profile.html",
							  {"loggedInUser": loggedInUser, "profile": profile, "gravatar": gravatarMD5,
							   'approvals': [], 'taxonomyItems': taxonomyItems, 'notifications': []},
							  context_instance=RequestContext(request))


@login_required
def profile(request):
	if request.user.is_authenticated():
		requestedUser = request.user
		loggedInUser = True
	else:
		return render_to_response("infopage.html",
								  {"messageTitle": "You must be logged in to view this page",
								   "messageBody": "Please log in before attempting to view this content."},
								  context_instance=RequestContext(request))

	profile = None

	try:
		if not requestedUser.get_profile() is None:
			profile = requestedUser.get_profile()
	except:
		profile = UserProfile(user=requestedUser)
		profile.save()

	gravatarMD5 = None
	if profile.gravatarEmail:
		gravatarMD5 = hashlib.md5(profile.gravatarEmail).hexdigest()

	approvals = []
	if requestedUser.is_superuser:
		approvalsQuery = OwnershipRequest.objects.all()
		for approvalQueryResultItem in approvalsQuery:
			approvals.append(approvalQueryResultItem)

	taxonomyItems = []

	notifications = []
	taxonomyItemsForUser = TaxonomyItem.objects.filter(owners__username=requestedUser.username)

	for userTaxonomyItem in taxonomyItemsForUser:
		taxonomyItems.append(userTaxonomyItem)
		enquiryQueryForTaxonomyItem = Enquiry.objects.filter(taxonomyItem=userTaxonomyItem)

		for enquiry in enquiryQueryForTaxonomyItem:
			notifications.append(enquiry)

	requestedTaxonomyItemsForUser = OwnershipRequest.objects.filter(requester__username=requestedUser.username)

	return render_to_response("profile.html",
							  {"loggedInUser": loggedInUser, "profile": profile, "gravatar": gravatarMD5,
							   'approvals': approvals, 'taxonomyItems': taxonomyItems,
							   'requested': requestedTaxonomyItemsForUser, 'notifications': notifications},
							  context_instance=RequestContext(request))


def orcid_profile(request):
	orcid = request.GET['orcid']

	request = urllib2.Request('http://pub.orcid.org/' + orcid + "/orcid-profile",
							  headers={"Accept": "application/orcid+json"})
	response = urllib2.urlopen(request).read()

	return HttpResponse(response, mimetype='application/json')


def sendEmailForEnquiry(message, request, taxonomyItem):
	try:
		email_subject = email_prefix + "Message received by " + request.user.username + " for taxonomy item " + taxonomyItem.name
		email_from = request.user.email

		url = Site.objects.filter(id=SITE_ID).get(id=SITE_ID).domain

		email_body = 'You can view this taxonomy item <a href=\"' + url + '/taxonomy/' + str(
			taxonomyItem.id) + '\">here</a>.\n\n'

		email_body += message

		send_mail(email_subject, email_body, email_from,
				  [EMAIL_HOST_USER], fail_silently=False)
	except Exception, e:
		return render_to_response("templates/infopage.html",
								  {
								  'messageTitle': 'Problem encountered sending the request.',
								  'messageBody': "There was a problem sending the email. Please ensure all fields "
												 "are filled in correctly. Please contact " +
												 settings.ADMINS[0][1]
												 + " if the problem continues.\n\nDetailed reason is below: \n\n"
												 + e.message},
								  context_instance=RequestContext(request))
	else:
		return render_to_response("templates/infopage.html",
								  {'messageTitle': 'Your suggestion for ' + taxonomyItem.name + ' has been lodged.',
								   'messageBody': "The maintainer will get back to you soon!"},
								  context_instance=RequestContext(request))


def getTaxonomyTree(request, formatting):
	taxonomy = []
	taxonomyArea = TaxonomyArea.objects.filter(name="Visualisation").get(name="Visualisation")
	categories = taxonomyArea.taxonomycategory_set.all()

	if formatting == "jsTree":
		for category in categories:
			items = []
			for item in category.taxonomyitem_set.all():
				items.append({"data": item.name + " (" + str(len(item.references())) + " refs)",
					"attr": {"itemId": item.id, "type": "taxonomyItem", "level":0}})

			if category.taxonomycategory_set:
				for subCategory in category.taxonomycategory_set.all():
					sub_items = []
					for item in subCategory.taxonomyitem_set.all():
						sub_items.append({"data": item.name + " (" + str(len(item.references())) + " refs)",
							"attr": {"itemId": item.id, "type": "taxonomyItem", "level":1}})

					items.append(
						{"data": subCategory.name, "attr": {"itemId": subCategory.id, "type": "taxonomyCategory"},
						 "children": sub_items, "state": "closed"})

			taxonomy.append(
				{"data": category.name, "attr": {"itemId": category.id, "type": "taxonomyCategory"}, "children": items,
				 "state": "closed"})

		response = [{"data": "Taxonomy", "children": taxonomy, "state": "open"}]

	else:
		for category in categories:
			items = []
			for item in category.taxonomyitem_set.all():
				items.append({"data": item.name + " (" + str(len(item.references())) + " refs)", "id": item.id})

			if category.taxonomycategory_set:
				sub_items = []
				for subCategory in category.taxonomycategory_set.all():
					for item in subCategory.taxonomyitem_set.all():
						sub_items.append(
							{"data": item.name + " (" + str(len(item.references())) + " refs)", "id": item.id})

					items.append({"data": subCategory.name, "children": sub_items})

			taxonomy.append({"data": category.name, "children": items})

		response = {"taxonomy": taxonomy}

	return HttpResponse(simplejson.dumps(response), mimetype="application/json")


def getTaxonomyCategories(request):
	categories = TaxonomyCategory.objects.all()
	categoryArray = []

	for category in categories:
		categoryArray.append({"id": category.id, "name": category.name})

	response = {"categories": categoryArray}
	return HttpResponse(simplejson.dumps(response), mimetype="application/json")


def getTaxonomyCategoryJSON(request, taxonomy_id):
	taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)

	referenceQuery = taxonomy.references()
	references = taxonomy.references()

	hasOwner = False

	if len(taxonomy.owners.all()) > 0:
		hasOwner = True

	ownerLoggedIn = False
	if request.user in taxonomy.owners.all():
		ownerLoggedIn = True

	count = len(references)
	refjsonlist = []

	for (ref_id, reference) in references:
		reference['url'] = URL_PREPENDER + "/reference/" + str(ref_id)
		print reference
		refjsonlist.append(reference);

	response = {"id": taxonomy.id, "name": taxonomy.name, "description": taxonomy.detail,
				"url": URL_PREPENDER + "/taxonomy/" + str(taxonomy.id),
				"hasOwner": hasOwner, "isOwner": ownerLoggedIn,
				"count": count, "references": refjsonlist}

	return HttpResponse(simplejson.dumps(response), mimetype="application/json")


def getTaxonomyCategoryInformationJSON(request, category_id):
	category = get_object_or_404(TaxonomyCategory, pk=category_id)
	taxonomyItems = category.taxonomyitem_set.all()

	taxonomyItemList = []

	for taxonomyItem in taxonomyItems:
		taxonomyItemList.append({"id": taxonomyItem.id, "title": taxonomyItem.name, "description": taxonomyItem.detail,
								 "url": URL_PREPENDER + "/taxonomy/" + str(taxonomyItem.id),
								 "referenceCount": len(taxonomyItem.references())})

	response = {"id": category.id, "name": category.name, "taxonomyItems": taxonomyItemList}

	return HttpResponse(simplejson.dumps(response), mimetype="application/json")

def moveTaxonomyItem(request, taxonomy_id):
	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)

	newCategory = request.POST.get('newCategory', '')

	print 'New category is ' + newCategory

	success = True
	message = 'The parent for ' + taxonomyItem.name + ' has been changed from ' + taxonomyItem.category.name + ' to ' + newCategory

	if newCategory:
		categoryQuery = TaxonomyCategory.objects.filter(name=newCategory)
		if len(categoryQuery) > 0:
			taxonomyItem.category = categoryQuery.get(name=newCategory)
			taxonomyItem.save()
	else:
		success = False
		message = 'An error occurred changing the taxonomy parent. Please select a taxonomy category.'

	return HttpResponseRedirect(URL_PREPENDER + "/taxonomy/?success=" + str(success) + "&message=" + str(message))


def renameTaxonomyCategoryAPI(request, category_id):
	category = TaxonomyCategory.objects.filter(pk=category_id).get(pk=category_id)
	newName = request.POST.get('newName', category.name)

	success = True
	message = 'Successfully renamed ' + category.name + ' to ' + newName

	category.name = newName
	category.save()

	return HttpResponseRedirect(URL_PREPENDER + "/taxonomy/?success=" + str(success) + "&message=" + str(message))


def handleTaxonomyEnquiry(request, taxonomy_id):
	type = request.POST['type']
	message = request.POST['message']

	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
	enquiry = Enquiry(taxonomyItem=taxonomyItem, requester=request.user, additionalNotes=message, enquiry_type=type)
	enquiry.save()

	return sendEmailForEnquiry(message, request, taxonomyItem)


@login_required
def handleReferenceEnquiry(request, taxonomy_id, reference_id):
	type = request.POST['type']
	message = request.POST['message']

	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
	referenceItem = Reference.objects.filter(pk=reference_id).get(pk=reference_id)

	enquiry = Enquiry(taxonomyItem=taxonomyItem, requester=request.user, additionalNotes=message, enquiry_type=type,
					  reference=referenceItem)
	enquiry.save()

	return sendEmailForEnquiry(message, request, taxonomyItem)


@login_required
def respondToTaxonomyEnquiry(request, decision, enquiry_id):
	message = request.POST['message']

	enquiryItem = Enquiry.objects.filter(pk=enquiry_id).get(pk=enquiry_id)

	email_subject = email_prefix + "Suggestion for " + enquiryItem.taxonomyItem.name + " " + decision

	email_body_prefix = "Many thanks for your suggestion. Here is the response from the maintainer!\n\n"
	email_body_reason = message

	try:
		send_mail(email_subject, email_body_prefix + email_body_reason,
				  EMAIL_HOST_USER,
				  [enquiryItem.requester.email], fail_silently=False)

	except Exception, e:
		return render_to_response("templates/infopage.html",
								  {
								  'messageTitle': 'Problem encountered sending the message to ' + enquiryItem.requester.email + '.',
								  'messageBody': "Here are the details\n." + e.message},
								  context_instance=RequestContext(request))
	finally:
		enquiryItem.delete()

	return render_to_response("templates/infopage.html",
							  {
							  'messageTitle': 'Response lodged.',
							  'messageBody': 'Response lodged and suggester has been emailed at ' + enquiryItem.requester.email + '.'},
							  context_instance=RequestContext(request))


def taxonomy_add(request):
	categories = TaxonomyCategory.objects.all()
	return render_to_response("templates/taxonomy_edit_base.html", {'categories': categories},
							  context_instance=RequestContext(request))


def taxonomy_edit(request, taxonomy_id):
	categories = TaxonomyCategory.objects.all()
	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
	return render_to_response("templates/taxonomy_edit_base.html", {'taxonomy': taxonomyItem, 'categories': categories},
							  context_instance=RequestContext(request))


def taxonomy_delete(request, taxonomy_id):
	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
	taxonomyItem.delete()
	# for now, any attached references are left dangling
	return HttpResponseRedirect(URL_PREPENDER + "/taxonomy/")


def taxonomy_split(request, taxonomy_id):
	taxonomyItemToSplit = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)

	newTaxonomyItem = request.POST.get('newTaxonomyName', '')

	success = True
	message = 'The splitting of ' + taxonomyItemToSplit.name + ' was successful. ' + newTaxonomyItem + \
			  ' is now available for your perusal.'

	try:
		if newTaxonomyItem is None or len(newTaxonomyItem) == 0 or taxonomyItemToSplit is None:
			raise Exception

		ref_lists = [request.POST.get('originalTaxonomyReferences', '').split(','),
					 request.POST.get('newTaxonomyReferences', '').split(',')]

		# create new taxonomy item
		newTaxonomyItem = TaxonomyItem(name=newTaxonomyItem, category=taxonomyItemToSplit.category)
		newTaxonomyItem.save()

		curr_refs = taxonomyItemToSplit.reference_family().get_references_as_dict()

		# go through each ref and move over to new family if necessary
		for ref_id, ref_doc in curr_refs:
			if ref_id in ref_lists[1]:
				taxonomyItemToSplit.reference_family().move_reference(ref_id, newTaxonomyItem.reference_family())
	except Exception, e:
		success = False
		message = 'The splitting of ' + taxonomyItemToSplit.name + ' was unsuccessful. Please try again.'

	return HttpResponseRedirect(URL_PREPENDER + "/taxonomy/?success=" + str(success) + "&message=" + str(message))


def taxonomy_add_child(request, taxonomy_id):
	taxItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
	newChildName = request.POST.get("newChildName", "")
	parentName = taxItem.name

	try:
		if len(newChildName) == 0 or taxItem is None:
			raise Exception

		# create category with same name as this item
		cat = TaxonomyCategory(name=taxItem.name,parent=taxItem.category)
		cat.save();

		# create new child item (weird method but seems to be how you to copy model instances in Django)
		new_child = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
		new_child.pk = None
		new_child.save()
		new_child.name = newChildName
		new_child.category = cat
		new_child.save()

		# shift references old -> new item
		taxItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
		taxItem.reference_family().move_all_references(new_child.reference_family())

		# finally kill the existing child
		taxItem.delete()

		message = "Created new taxonomy item named %s of parent %s" % (newChildName, parentName)
		success = True
	except Exception, e:
		success = False
		message = "There was a problem creating the child node. Please contact us. Details: " + str(e)

	return HttpResponseRedirect(URL_PREPENDER + "/taxonomy/?success=" + str(success) + "&message=" + str(message))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def moveReferences(request):
	tax_ids = [request.POST.get('moveRefFromTaxonomy', ''), request.POST.get('moveRefToTaxonomy', '')]
	new_ref_list = [request.POST.get('moveFromTaxonomyReferences', '').split(","),
					request.POST.get('moveToTaxonomyReferences', '').split(",")]

	try:
		if tax_ids[0] == tax_ids[1]:
			raise Exception

		taxonomy = []
		families = []
		old_refs = []
		for tax in range(0, 2):
			taxonomy.append(TaxonomyItem.objects.filter(pk=tax_ids[tax]).get(pk=tax_ids[tax]))
			families.append(taxonomy[tax].reference_family())
			old_refs.append(families[tax].get_references_as_dict())

		refs_moved = 0
		for tax in range(0, 2):
			source = tax
			dest = (tax + 1) % 2
			for ref_id, ref_doc in old_refs[source]:
				# the old ref from this family is in t'other list, then move it move it move it
				if ref_id in new_ref_list[dest]:
					print "Moving source %i dest %i" % (source, dest)
					print "Ref id " + ref_id
					families[source].move_reference(ref_id, families[dest])
					refs_moved += 1

		success = True
		message = 'The moving of %i references between %s and %s was successful!' % (
		refs_moved, taxonomy[0].name, taxonomy[1].name)
	except Exception, e:
		success = False
		message = 'The moving of references between the taxonomies was unsuccessful. Please try again.'

	return HttpResponseRedirect(URL_PREPENDER + "/taxonomy/?success=" + str(success) + "&message=" + str(message))


@login_required()
def taxonomy_add_action(request):
	name = request.POST.get('taxonomy_name', None)
	category = request.POST.get('category_name', None)
	detail = request.POST.get('description', None)

	categoryObject, existed = TaxonomyCategory.objects.get_or_create(name=category)
	taxonomy = TaxonomyItem(name=name, category=categoryObject, detail=detail, last_updated=datetime.now())
	taxonomy.last_updated_by = request.user

	taxonomy.save()

	return HttpResponseRedirect(URL_PREPENDER + "/taxonomy/" + str(taxonomy.id))


def trimURL(urlRequestedFrom, find):
	return urlRequestedFrom[0:urlRequestedFrom.find(find)]


@login_required()
def taxonomy_edit_action(request):
	taxonomyId = request.POST.get('taxonomy_id', None)
	name = request.POST.get('taxonomy_name', None)
	category = request.POST.get('category_name', None)
	detail = request.POST.get('description', None)
	urlRequestedFrom = request.POST.get('postedFrom', '/')

	urlRequestedFrom = trimURL(urlRequestedFrom, 'edit') + taxonomyId

	categoryObject, existed = TaxonomyCategory.objects.get_or_create(name=category)

	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomyId).get(pk=taxonomyId)
	taxonomyItem.name = name
	taxonomyItem.category = categoryObject
	taxonomyItem.detail = detail
	taxonomyItem.last_updated = datetime.now()
	taxonomyItem.last_updated_by = request.user

	taxonomyItem.save()

	return HttpResponseRedirect(urlRequestedFrom)


@login_required
def reference_add_upload_file(request):
	taxonomy_id = request.POST.get('taxonomy_id', None)
	urlRequestedFrom = request.POST.get('postedFrom', '/')

	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)

	bibtex_file_upload = request.FILES['bibtex_file']

	try:
		bibtextFile = saveFile(bibtex_file_upload)
		bibtex_import(bibtextFile, taxonomyItem)
		taxonomyItem.last_updated = datetime.now()
		taxonomyItem.save()

		return HttpResponseRedirect(urlRequestedFrom)
	except Exception, e:
		return render_to_response("templates/infopage.html",
								  {
								  'messageTitle': 'Error in bibtex import.',
								  'messageBody': 'We\'ve not been able to import the file you selected. Please ensure it\'s valid BibTeX.\n\n' + e.message},
								  context_instance=RequestContext(request))


@login_required
def reference_add_upload_text(request):
	taxonomy_id = request.POST.get('taxonomy_id', None)
	urlRequestedFrom = request.POST.get('postedFrom', '/')

	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)

	bibtex_contents = request.POST.get('bibtex', '')

	try:
		bibtextFile = saveTextToFile(bibtex_contents)
		bibtex_import(bibtextFile, taxonomyItem)
		taxonomyItem.last_updated = datetime.now()
		taxonomyItem.save()
		return HttpResponseRedirect(urlRequestedFrom)

	except Exception, e:
		return render_to_response("templates/infopage.html",
								  {
								  'messageTitle': 'Error in bibtex import.',
								  'messageBody': 'We\'ve not been able to import the text you entered. Please ensure it\'s valid bibtex.\n\n' + e.message},
								  context_instance=RequestContext(request))


def contact_send(request):
	email_subject = email_prefix + "Contact"
	email_from = request.POST.get('email', '')
	email_name = request.POST.get('name', '')
	email_body = request.POST.get('comments', '')

	if email_body == '':
		return render_to_response("templates/contact.html",
								  {
								  'error_message': "No message was given. This is required, as I'm sure you'll understand. "},
								  context_instance=RequestContext(request))

	try:
		headers = {'Reply-To': email_from}
		email_body = 'Message sent from ' + email_name + ' (' + email_from + ')\n\n' + email_body

		message = EmailMessage(email_subject, email_body, email_from, [item[1] for item in settings.ADMINS],
							   headers=headers)
		message.send(fail_silently=False)
	except Exception, e:
		return render_to_response("templates/contact.html",
								  {
								  'error_message': "There was a problem sending the email. Please ensure all fields are filled in correctly. Please contact " +
												   settings.ADMINS[0][1] + " if the problem continues."},
								  context_instance=RequestContext(request))
	else:
		return render_to_response("templates/contact.html", {'success_message': 'Your request was sent successfully!'},
								  context_instance=RequestContext(request))


@login_required
def reference_remove(request, taxonomy_id, reference_id):
	urlRequestedFrom = request.POST.get('postedFrom', '/')

	taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
	taxonomyItem.remove_reference(reference_id)

	return HttpResponseRedirect(urlRequestedFrom)


@login_required
def reference_delete(request, taxonomy_id, reference_id):
	print "Deleting"
	referenceItem = ReferenceGlobal().remove_reference(taxonomy_id, reference_id)

	return render_to_response("templates/infopage.html",
							  {
							  'messageTitle': 'Reference deleted successfully.',
							  'messageBody': 'We\'ve deleted that reference for you.'},
							  context_instance=RequestContext(request))


def reference_detail(request, taxonomy_id, reference_id):
	currentPage = request.GET.get('currentPage', '')

	referenceItem = {}
	assignedTaxonomyItem = {}

	try:
		referenceItem = ReferenceGlobal().get_reference(taxonomy_id, reference_id)
		assignedTaxonomyItem = TaxonomyItem.objects.get(pk=taxonomy_id)
		print assignedTaxonomyItem
	except Exception, e:
		logger.error('Bit of a mishap. Here is the error: ', str(e.message))

	return render_to_response("templates/reference.html",
							  {'reference': referenceItem, 'taxonomy_item': assignedTaxonomyItem,
							   'previousPage': currentPage},
							  context_instance=RequestContext(request))


@login_required
def volunteer(request):
	"""
	Shows a page with a form listing the taxonomy items available to manage.
	"""
	taxonomyItemsWithNoOwnerQuery = TaxonomyItem.objects.filter(owners=None)

	#the results go in to a dictionary so that we can build a nested tree of categories to taxonomy items
	resultDict = {}

	for taxonomyItem in taxonomyItemsWithNoOwnerQuery:
		if not resultDict.has_key(taxonomyItem.category.name):
			resultDict[taxonomyItem.category.name] = []

		resultDict[taxonomyItem.category.name].append(taxonomyItem)

	return render_to_response("templates/volunteer.html",
							  {'available': resultDict}, context_instance=RequestContext(request))


def server_error(request, template_name='500.html'):
	return render_to_response(template_name, context_instance=RequestContext(request))


