"""
 Data models
"""

from django.contrib.auth.models import User
from django.db import models
import user
import reference_backend


class ReferenceAuthor(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256)
    prelast_name = models.CharField(max_length=256)
    lineage = models.CharField(max_length=256)

    def __unicode__(self):
        return self.first_name + ", " + self.last_name + ", " + self.lineage


class ReferenceColumn(models.Model):
    name = models.CharField(max_length=128)


class ReferenceAttribute(models.Model):
    column = models.ForeignKey(ReferenceColumn)
    value = models.TextField(default="")

    def __unicode__(self):
        return self.column.name + " (" + self.value + ")"


class Reference(models.Model):
    entry_key = models.CharField(max_length=256)
    title = models.TextField(default="")
    journal = models.CharField(max_length=256, default="")
    year = models.IntegerField(max_length=4, null=True)
    url = models.CharField(max_length=256, default="")

    authors = models.ManyToManyField(ReferenceAuthor, related_name="authors+")
    bibtex = models.TextField()
    referenceAttributes = models.ManyToManyField(ReferenceAttribute, related_name="attributes+")

    date_added = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)

    def __unicode__(self):
        return self.entry_key + " - " + self.title


class TaxonomyArea(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class TaxonomyCategory(models.Model):
    name = models.CharField(max_length=128)
    area = models.ForeignKey(TaxonomyArea)

    def __unicode__(self):
        return self.name + " (" + self.area.name + ")"


class TaxonomyItem(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(TaxonomyCategory)
    detail = models.TextField(default="")
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(User, null=True)
    owners = models.ManyToManyField(User, related_name="owners+")

    references = models.ManyToManyField(Reference)

    def short_description(self):
        return self.detail[:50] + '...'

    def __unicode__(self):
        return self.name + " (" + self.category.name + ")"


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    orcid = models.CharField(max_length=19, blank=True)
    gravatarEmail = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return user

    def get_absolute_url(self):
        return 'profiles_profile_detail', (), {'username': self.user.username}

    get_absolute_url = models.permalink(get_absolute_url)


class OwnershipRequest(models.Model):
    requester = models.ForeignKey(User)
    taxonomyItem = models.ForeignKey(TaxonomyItem)
    additionalNotes = models.TextField()

    def __unicode__(self):
        return self.requester.username + ' - ' + self.taxonomyItem.name

class Enquiry(models.Model):

    requester = models.ForeignKey(User)
    taxonomyItem = models.ForeignKey(TaxonomyItem)
    enquiry_type = models.CharField(max_length=256, default="")
    # optional
    reference = models.ForeignKey(Reference, null=True)
    additionalNotes = models.TextField()
