"""
 Views - see urls.py for the mappings from URLs to the defs here.
"""
import hashlib
import urllib2
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from viscommunityweb.settings import EMAIL_HOST_USER, SITE_ID
from web.models import TaxonomyArea, TaxonomyCategory, TaxonomyItem, Reference, UserProfile, OwnershipRequest, Enquiry
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
import os
from django.conf import settings
import taxonomy_backend, reference_backend
import json

# couple of globals
os.environ['DJANGO_SETTINGS_MODULE'] = "viscommunityweb.settings"
email_prefix = "[OXVIS] "
email_to = "eamonn.maguire@oerc.ox.ac.uk"


# index page
def index(request):
    recent_items = TaxonomyItem.objects.order_by('last_updated')[:3]
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

    references = taxonomy.references.all()

    refer = reference_backend.sorted_reference_list(request, references)

    ownerLoggedIn = False
    if request.user in taxonomy.owners.all():
        ownerLoggedIn = True

    return render_to_response("templates/taxonomy_detail.html",
                              {'taxonomy': taxonomy, 'owners': len(taxonomy.owners.all()),
                               'ownerLoggedIn': ownerLoggedIn, 'references': refer},
                              context_instance=RequestContext(request))


def taxonomy_download(request, taxonomy_id):
    taxonomy = get_object_or_404(TaxonomyItem, pk=taxonomy_id)

    references = taxonomy.references.all()

    bibtex = ""

    for reference in references:
        bibtex += reference.bibtex + "\n"

    response = HttpResponse(bibtex, mimetype='application/text')
    response['Content-Disposition'] = 'attachment; filename=' + taxonomy.name + ".bib"
    return response


# general contact page
def contact(request):
    return render_to_response("templates/contact.html", context_instance=RequestContext(request))


# accessed through a POST to send email to the admins regarding above
def request_ownership_send(request, taxonomy_id):
    email_subject = email_prefix + "Request for taxonomy ownership by " + request.user.username
    email_from = request.user.email
    email_body = request.POST['comments']

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

    ownershipRequest = OwnershipRequest.objects.filter(pk=approval_id).get(pk=approval_id)

    taxonomyItem = ownershipRequest.taxonomyItem
    if response == 'Approved':
        ownershipRequest = OwnershipRequest.objects.filter(pk=approval_id).get(pk=approval_id)
        taxonomyItem = ownershipRequest.taxonomyItem
        taxonomyItem.owners.add(ownershipRequest.requester)
        taxonomyItem.save()

    email_subject = email_prefix + "Request for ownership of " + taxonomyItem.name + " " + response

    email_body_prefix = "We are pleased to welcome you on board Community Vis!\n\n"
    if response != "Approved":
        email_body_prefix = "We are sorry to inform you that we were unable to approve your request.!\n\n"

    email_body_reason = responseDetail

    try:
        send_mail(email_subject, email_body_prefix + email_body_reason,
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

    return HttpResponseRedirect("/accounts/profile")


@login_required
def revoke_ownership(request, taxonomy_id):
    reason = request.POST['comments']

    taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)

    taxonomyItem.owners.remove(request.user)

    try:
        email_subject = email_prefix + "Ownership revoked by " + request.user.username + " for " + taxonomyItem.name
        email_from = request.user.email
        email_name = request.user.username
        email_body = request.POST['comments']

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
def references(request):
    refs = reference_backend.sorted_reference_list(request)

    return render_to_response("templates/references.html",
                              {'references': refs, 'bibtex_texts': json.dumps([x.bibtex for x in refs])},
                              context_instance=RequestContext(request))


# search
def search(request):
    searchTerm = request.GET['q']
    references = Reference.objects.all()

    searchResult = []

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
    requestedUser = None
    loggedInUser = False

    if request.user.is_authenticated:
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



    return render_to_response("profile.html",
                              {"loggedInUser": loggedInUser, "profile": profile, "gravatar": gravatarMD5,
                               'approvals': approvals, 'taxonomyItems': taxonomyItems, 'notifications': notifications},
                              context_instance=RequestContext(request))


def orcid_profile(request):
    orcid = request.GET['orcid']

    request = urllib2.Request('http://pub.orcid.org/' + orcid + "/orcid-profile",
                              headers={"Accept": "application/orcid+json"})
    response = urllib2.urlopen(request).read()

    return HttpResponse(response, mimetype='application/json')


@login_required
def handleTaxonomyEnquiry(request, taxonomy_id):
    type = request.POST['type']
    message = request.POST['message']

    taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
    enquiry = Enquiry(taxonomyItem=taxonomyItem, requester=request.user, additionalNotes=message, enquiry_type=type)
    enquiry.save()

    try:
        email_subject = email_prefix + "Message received by " + request.user.username + " for taxonomy item " + taxonomyItem.name
        email_from = request.user.email

        url = Site.objects.filter(id=SITE_ID).get(id=SITE_ID).domain

        email_body = "You can view this taxonomy item <a href=" + url + "/taxonomy/" \
                     + taxonomyItem.id + ">here</a>.\n\n"

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
                                  {'messageTitle': 'You suggestion for ' + taxonomyItem.name + ' has been lodged.',
                                   'messageBody': "The maintainer will get back to you soon!"},
                                  context_instance=RequestContext(request))
