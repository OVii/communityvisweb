"""
 Views - see urls.py for the mappings from URLs to the defs here.
"""
from datetime import datetime
import hashlib
import urllib2
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from viscommunityweb.settings import EMAIL_HOST_USER, SITE_ID
from web.bibtex_utils.import_utils import saveFile, saveTextToFile
from web.models import TaxonomyCategory, TaxonomyItem, Reference, UserProfile, OwnershipRequest, Enquiry
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
import os
from django.conf import settings
import taxonomy_backend, reference_backend
import json

# couple of globals
from web.reference_import import bibtex_import

os.environ['DJANGO_SETTINGS_MODULE'] = "viscommunityweb.settings"
email_prefix = "[OXVIS] "
email_to = "eamonn.maguire@oerc.ox.ac.uk"


# index page
def index(request):
    recent_items = TaxonomyItem.objects.order_by('-last_updated')[:3]
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
    allReferences = Reference.objects.all()

    references = [reference_backend.SortableReference(x) for x in allReferences]
    return render_to_response("templates/search.html",
                              {"searchTerm": searchTerm, "size": len(references), "searchResults": references},
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

    requestedUser = None
    loggedInUser = False

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
    except:
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


def sendEmailForEnquiry(message, request, taxonomyItem):
    try:
        email_subject = email_prefix + "Message received by " + request.user.username + " for taxonomy item " + taxonomyItem.name
        email_from = request.user.email

        url = Site.objects.filter(id=SITE_ID).get(id=SITE_ID).domain

        email_body = "You can view this taxonomy item <a href=" + url + "/taxonomy/" \
                     + str(taxonomyItem.id) + ">here</a>.\n\n"

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


@login_required
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


@login_required()
def taxonomy_add_action(request):
    name = request.POST.get('taxonomy_name', None)
    category = request.POST.get('category_name', None)
    detail = request.POST.get('description', None)

    print 'Name ' + name + " - Category " + category

    categoryObject, existed = TaxonomyCategory.objects.get_or_create(name=category)
    taxonomy = TaxonomyItem(name=name, category=categoryObject, detail=detail, last_updated=datetime.now())
    taxonomy.last_updated_by = request.user

    taxonomy.save()

    return taxonomy_detail(request, taxonomy.id)


@login_required()
def taxonomy_edit_action(request):
    taxonomyId = request.POST.get('taxonomy_id', None)
    name = request.POST.get('taxonomy_name', None)
    category = request.POST.get('category_name', None)
    detail = request.POST.get('description', None)

    categoryObject, existed = TaxonomyCategory.objects.get_or_create(name=category)

    taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomyId).get(pk=taxonomyId)
    taxonomyItem.name = name
    taxonomyItem.category = categoryObject
    taxonomyItem.detail = detail
    taxonomyItem.last_updated = datetime.now()
    taxonomyItem.last_updated_by = request.user

    taxonomyItem.save()

    return taxonomy_detail(request, taxonomyId)


def reference_add_upload_file(request):
    taxonomy_id = request.POST.get('taxonomy_id', None)

    taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)

    bibtex_file_upload = request.FILES['bibtex_file']

    try:
        bibtextFile = saveFile(bibtex_file_upload)
        bibtex_import(bibtextFile, taxonomyItem)
        taxonomyItem.last_updated = datetime.now()
        taxonomyItem.save()
        return HttpResponseRedirect("/taxonomy/" + taxonomy_id)
    except Exception, e:
        return render_to_response("templates/infopage.html",
                                  {
                                      'messageTitle': 'Error in bibtex import.',
                                      'messageBody': 'We\'ve not been able to import the file you selected. Please ensure it\'s valid.\n\n' + e.message},
                                  context_instance=RequestContext(request))


def reference_add_upload_text(request):
    taxonomy_id = request.POST.get('taxonomy_id', None)

    taxonomyItem = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)

    bibtex_contents = request.POST.get('bibtex', '')

    try:
        bibtextFile = saveTextToFile(bibtex_contents)
        bibtex_import(bibtextFile, taxonomyItem)
        taxonomyItem.last_updated = datetime.now()
        taxonomyItem.save()
        return HttpResponseRedirect("/taxonomy/" + taxonomy_id)

    except Exception, e:
        return render_to_response("templates/infopage.html",
                                  {
                                      'messageTitle': 'Error in bibtex import.',
                                      'messageBody': 'We\'ve not been able to import the text you entered. Please ensure it\'s valid bibtex.\n\n' + e.message},
                                  context_instance=RequestContext(request))


def contact_send(request):
    email_subject = email_prefix + "Contact"
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
