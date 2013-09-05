import uuid
import pycassa
from pycassa.system_manager import *
import hashlib
from pycassa.types import *
from pycassa.columnfamilymap import ColumnFamilyMap
from datetime import datetime
from pycassa.index import *

"""

use community_refs;
create column family reference with comparator = UTF8Type and key_validation_class = UTF8Type and default_validation_class = UTF8Type;

"""

KEYSPACE = "community_refs"

pool = pycassa.ConnectionPool(KEYSPACE)

"""class ReferenceAuthor(object):
	def __init__(self):
		self.key = str(uuid.uuid1())

	def save(self):
		reference_map.insert(self)

	key = UTF8Type()
	first_name = UTF8Type()
	last_name = UTF8Type()
	middle_name = UTF8Type()
	prelast_name = UTF8Type()
	lineage = UTF8Type()

class ReferenceAttribute(object):
	def __init__(self, ref_obj, col, val):
		self.key = str(uuid.uuid1())
		self.ref_key = ref_obj.key
		self.col = col
		self.val = val

	def save(self):
		attribute_map.insert(self)

	@staticmethod
	def get_all_for_ref(ref_obj):
		clause = create_index_clause(create_index_expression('ref_key',ref_obj.key))
		return reference_attributes.get_indexed_slices(clause)

	ref_key = UTF8Type()
	col = UTF8Type()
	val = UTF8Type()

# Reference / Author many-to-many
class ReferenceMMAuthor(object):
	key = UTF8Type()
	ref_key = UTF8Type()
	author_key = UTF8Type()
"""
class Reference(object):
	@staticmethod
	def ref_hash(bib_key, ref_title):
		return unicode(str(hashlib.sha224(bib_key + '_' + ref_title).hexdigest()[:16]),'utf-8')

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


#author_map = ColumnFamilyMap(ReferenceAuthor, pool, 'ReferenceAuthor')
#attribute_map = ColumnFamilyMap(ReferenceAttribute, pool, 'ReferenceAttribute')
#reference_mm_author_map = ColumnFamilyMap(ReferenceMMAuthor, pool, 'ReferenceMMAuthor')
# cassandra-cli
# [default@community_refs] create column family reference and comparitor = 'AsciiType'#


# Reference Family - one per Taxonomy Item (as identified by its guid)
class ReferenceFamily:
	def __init__(self, string):
		self.guid = str(hashlib.sha224(string).hexdigest()[:16])
		self.pool = pool
		self.ensure_exists()
		self.colmap = ColumnFamilyMap(Reference, self.pool, self.guid)

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

