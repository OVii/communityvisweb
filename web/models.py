
"""
 Data models
"""

from django.contrib.auth.models import User
from django.db import models
import reference_backend

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
	name = models.CharField(max_length=128)
	category = models.ForeignKey(TaxonomyCategory)
	detail_html = models.CharField(max_length=2048)
	last_updated = models.DateTimeField(auto_now=True)
	last_updated_by = models.ForeignKey(User, null=True)
	owners = models.ManyToManyField(User, related_name="owners+")

	def has_detail(self):
		return len(self.detail_html) != 0

	def short_description(self):
		return self.detail_html[:50] + '...'

	def __unicode__(self):
		return self.name + " (" + self.category.name + ")"

"""class UserTaxonomyItemOwnership(models.Model):
	user = models.ForeignKey(User)
	item = models.ForeignKey(TaxonomyItem)

	def __unicode__(self):
		return self.user.__unicode__() + " owns " + item.__unicode__()
"""

class ReferenceAuthor(models.Model):
	first_name = models.CharField(max_length=256)
	last_name = models.CharField(max_length=256)
	middle_name = models.CharField(max_length=256)
	prelast_name = models.CharField(max_length=256)
	lineage = models.CharField(max_length=256)

class ReferenceColumn(models.Model):
	name = models.CharField(max_length=128)	

class Reference(models.Model):
	bibtex = models.CharField(max_length=2048)
	entry_key = models.CharField(max_length=256)
	authors = models.ManyToManyField(ReferenceAuthor, related_name="authors+")
	#attributes = models.ManyToManyField(ReferenceAttribute, related_name="attributes+")

	def __unicode__(self):
		return self.bibtex

class ReferenceAttribute(models.Model):
	column = models.ForeignKey(ReferenceColumn)
	value = models.CharField(max_length=4096)
	reference = models.ForeignKey(Reference)


