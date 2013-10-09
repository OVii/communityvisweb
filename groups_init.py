
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from web.models import *

"""
 Groups
"""

moderator = Group(name="moderator")
moderator.save()
moderator.permissions.add(Permission.objects.get(
	content_type=ContentType.objects.get_for_model(OwnershipRequest),codename='respond_to_ownership_requests'))
moderator.permissions.add(Permission.objects.get(
	content_type=ContentType.objects.get_for_model(OwnershipRequest),codename='view_ownership_requests'))
moderator.permissions.add(Permission.objects.get(
	content_type=ContentType.objects.get_for_model(OwnershipRequest),codename='view_historical_ownership_requests'))
moderator.permissions.add(Permission.objects.get(
	content_type=ContentType.objects.get_for_model(TaxonomyItem),codename='revoke_ownership'))
moderator.save()

taxonomer = Group(name="taxonomer")
taxonomer.save()
taxonomer.permissions.add(Permission.objects.get(
	content_type=ContentType.objects.get_for_model(TaxonomyItem),codename='modify_taxonomy_items'))
taxonomer.permissions.add(Permission.objects.get(
	content_type=ContentType.objects.get_for_model(TaxonomyCategory),codename='modify_taxonomy_categories'))
taxonomer.save()

