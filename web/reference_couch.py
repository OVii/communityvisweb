import uuid
import hashlib
from datetime import datetime
from couchdb import *
import json

server = Server("http://127.0.0.1:5984/")

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

recent_references = None

# Reference Family - one per Taxonomy Item (as identified by its guid)
class ReferenceFamily(object):
	def __init__(self, tax_id):
		self.db = None
		self.tax_id = str(tax_id)
		self.ensure_exists()

	def database_id(self):
		return "ref_fam_%s" % self.tax_id

	def add_reference(self, ref):
		self.db.create(ref.__dict__)

	def get_reference(self, ref_id):
		return self.db[ref_id]

	def remove_reference(self, ref_id):
		self.db.delete(self.get_reference(ref_id))

	def ensure_exists(self):
		try:
			self.db = server[self.database_id()]
		except:
			self.db = server.create(self.database_id())
		assert(self.db is not None)

	def all_refs(self):
		return [(x.key, x.value) for x in self.db.query("function(d) { emit(d._id,d); }")]

class ReferenceFamilyQueue(ReferenceFamily):
	def __init__(self, size):
		super(ReferenceFamilyQueue,self).__init__(0)
		self.queue_size = size

	def database_id(self):
		return "ref_recent"

	def add_reference(self, ref):
		super(ReferenceFamilyQueue,self).add_reference(ref)
		self.limit_queue()

	def limit_queue(self):
		self.db.purge(self.db.query("function(d) { emit(d); }")[self.queue_size:])

recent_references = ReferenceFamilyQueue(3)
