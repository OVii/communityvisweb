import uuid
import pycassa
from pycassa.system_manager import *
import hashlib
from pycassa.types import *
from pycassa.columnfamilymap import ColumnFamilyMap
from pycassa.columnfamily import ColumnFamily
from datetime import datetime
from pycassa.index import *

"""

use community_refs;
create column family reference with comparator = UTF8Type and key_validation_class = UTF8Type and default_validation_class = UTF8Type;

"""

KEYSPACE = "community_refs"

pool = pycassa.ConnectionPool(KEYSPACE)

class Reference(object):
	@staticmethod
	def ref_hash(bib_key, ref_title):
		# key for reference: hash of the bib key and the title
		return unicode(str(hashlib.sha224(bib_key + '_' + ref_title).hexdigest()[:32]),'utf-8')

	def __init__(self):
		pass

	@staticmethod
	def create(family, bib_key, title):
		obj = Reference()
		obj.ref_map = family.reference_map()
		obj.key = Reference.ref_hash(bib_key, title)
		obj.entry_key = bib_key
		obj.title = title
		obj.bibtex = ''
		obj.year = ''
		obj.authorsAsText = ''
		obj.abstract = ''
		obj.journal = ''
		obj.year = 0
		obj.url = ''
		obj.date_added = datetime.now()
		return obj

	def save(self):
		self.ref_map.insert(self)

	@staticmethod
	def get_create_on_key_title(family, entry_key, title):
		h = Reference.ref_hash(entry_key, title)
		try:
			item = self.family.reference_map().get(h)
		except:
			item = Reference.create(family, entry_key, title)
		return item

	def __unicode__(self):
		return self.entry_key + ", " + self.title + " by " + self.authorsAsText + " in year " + str(self.year)

	key = UTF8Type()
	entry_key = AsciiType()
	title = AsciiType()
	authorsAsText =  AsciiType()
	abstract = AsciiType()
	journal = AsciiType()
	year = IntegerType()
	url = AsciiType()
	bibtex = AsciiType()
	date_added = DateType()

# Reference Family - one per Taxonomy Item (as identified by its guid)
class ReferenceFamily:
	def __init__(self, string):
		self.guid = str(hashlib.sha224(string).hexdigest()[:16])
		self.pool = pool
		self.ensure_exists()
		self.colmap = ColumnFamilyMap(Reference, self.pool, self.guid)
		self.tax_to_ref_family = ColumnFamily(self.pool, "tax_to_ref_family")

	# swap this reference family


	def reference_map(self):
		return self.colmap

	def ensure_exists(self):
		sys = SystemManager()
		try:
			sys.create_column_family(KEYSPACE, self.guid)
		except:
			pass

	def all_refs(self):
		return list(self.colmap.get_range())

class ReferenceDB:
	def add(self, guid, bibtex):
		fam = ReferenceFamily(guid)
		fam.add(bibtex)

	def refs_for_guid(self,guid):
		fam = ReferenceFamily(guid)
		return fam.all_refs()

