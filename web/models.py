"""
 Data models
"""

from django.contrib.auth.models import User
from django.db import models
import user
from reference_couch import *
import uuid
import hashlib
from datetime import datetime
from couchdb import *
import json

server = Server("http://127.0.0.1:5984/")



class TaxonomyArea(models.Model):
	name = models.CharField(max_length=128)

	def __unicode__(self):
		return self.name


class TaxonomyCategory(models.Model):
	name = models.CharField(max_length=128)
	area = models.ForeignKey(TaxonomyArea, null=True, blank=True)

	parent = models.ForeignKey('self', blank=True, null=True)

	def __unicode__(self):
		return self.name + " (" + self.area.name + ")"


class TaxonomyItem(models.Model):
	name = models.CharField(max_length=256)
	category = models.ForeignKey(TaxonomyCategory)
	detail = models.TextField(default="")
	last_updated = models.DateTimeField(auto_now=True)
	last_updated_by = models.ForeignKey(User, null=True)
	owners = models.ManyToManyField(User, related_name="owners+")

	def int_pk(self):
		try:
			return self.pk[0]
		except:
			return self.pk

	def references(self):
		return ReferenceFamily(self.int_pk()).all_refs()

	def remove_reference(self, ref_id):
		ReferenceFamily(self.int_pk()).remove_reference(ref_id)

	def short_description(self):
		return self.detail[:50] + '...'

	def __unicode__(self):
		return self.name + " (" + self.category.name + ")"


# represents a reference (duh)
class Reference(object):
	def __init__(self):
		self.entry_key = ''
		self.title = ''
		self.bibtex = ''
		self.year = ''
		self.authorsAsText = ''
		self.abstract = ''
		self.journal = ''
		self.year = 0
		self.url = ''
		self.date_added = str(datetime.now())

	def __unicode__(self):
		return self.entry_key + ", " + self.title + " by " + self.authorsAsText + " in year " + str(self.year)

# reference Family - one per TaxonomyItem (as identified by its id)
class ReferenceFamily(object):
	# initialise a reference family for a taxonomy id
	def __init__(self, tax_id):
		self.db = None
		self.tax_id = str(tax_id)
		self._ensure_exists()

	# name of this database object
	def database_id(self):
		return "ref_fam_%s" % self.tax_id

	# add a reference to this reference family
	def add_reference(self, ref):
		return self.db.create(ref.__dict__)

	# get a reference by id
	def get_reference(self, ref_id):
		return self.db[ref_id]

	# get all references
	def all_refs(self):
		return [(x.key, x.value) for x in self.db.query("function(d) { emit(d._id,d); }")]

	# remove a reference by id
	def remove_reference(self, ref_id):
		self.db.delete(self.get_reference(ref_id))

	# ensures db object exists; creates if not
	def _ensure_exists(self):
		try:
			self.db = server[self.database_id()]
		except:
			print "Creating database %s" % self.database_id()
			self.db = server.create(self.database_id())
		assert(self.db is not None)

# functions for dealing with references without worrying about which taxonomy they're attached to (ehh...)
class ReferenceGlobal(object):
	def __init__(self):
		self.all_tax_ids = [x.id for x in list(TaxonomyItem.objects.all())]

	def get_reference(self, tax_id, ref_id):
		return ReferenceFamily(tax_id).get_reference(ref_id)

	def tax_items_featuring_ref(self, ref_id):
		tax_ids = []
		for tax_id in self.all_tax_ids:
			try:
				tax_ids.append(ReferenceFamily(tax_id).get_reference(ref_id))
			except:
				pass
		return tax_ids

# represents a fixed-size queue of recent reference entries
class ReferenceFamilyQueue(ReferenceFamily):
	def __init__(self, size):
		super(ReferenceFamilyQueue,self).__init__(0)
		self.queue_size = size

	def database_id(self):
		return "ref_recent"

	def add_reference(self, ref, ref_id, tax_id):
		ref.ref_doc_id = ref_id
		ref.tax_id = tax_id
		super(ReferenceFamilyQueue,self).add_reference(ref)
		self.limit_queue()

	def limit_queue(self):
		self.db.purge(self.db.query("function(d) { emit(d); }")[self.queue_size:])

# front page recent references
recent_references = ReferenceFamilyQueue(3)

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
	#reference = models.ForeignKey(Reference, null=True)
	additionalNotes = models.TextField()
