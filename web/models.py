
"""
 Data models
"""

from django.contrib.auth.models import User
from django.db import models

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

	def has_detail(self):
		return len(self.detail_html) != 0

	def __unicode__(self):
		return self.name + " (" + self.category.name + ")"

class UserTaxonomyItemOwnership(models.Model):
	user = models.ForeignKey(User)
	item = models.ForeignKey(TaxonomyItem)

	def __unicode__(self):
		return self.user.__unicode__() + " owns " + item.__unicode__()

class Reference(models.Model):
	bibtex = models.CharField(max_length=2048)
	entry_id = models.CharField(max_length=256)

	def __unicode__(self):
		return self.bibtex
