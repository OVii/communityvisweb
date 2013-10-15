import logging
from web.models import *
import StringIO
from pybtex.bibtex.utils import bibtex_purify
from pybtex.database.input import bibtex as bib_in
from pybtex.database.output import bibtex as bib_out
from web.bibtex_utils.import_utils import saveTextToFile

logger = logging.getLogger(__name__)

def rescan_bibtex(taxonomy_id, reference_id):
	try:
		tax = TaxonomyItem.objects.filter(pk=taxonomy_id).get(pk=taxonomy_id)
		ref = ReferenceGlobal().get_reference(taxonomy_id, reference_id)
		print ref['bibtex']
		bibtextFile = saveTextToFile(ref['bibtex'])
		bibtex_edit(bibtextFile, taxonomy_id, ref)

		ref = ReferenceGlobal().get_reference(taxonomy_id, reference_id)
		print ref
	except Exception, e:
		print str(e)
	finally:
		tax.last_updated = datetime.now()
		tax.save()

def set_ref_from_entry(key, bib_data, ref_doc):
	stream = StringIO.StringIO()
	writer = bib_out.Writer(encoding='ascii')
	writer.write_entry(key, bib_data.entries[key], stream)
	ref_doc['bibtex'] = stream.getvalue()

	try:
		for field in bib_data.entries[key].fields:
			value = bib_data.entries[key].fields[field]

			fieldname = field.strip().lower()
			rawvalue = value
			value = bibtex_purify(value)
			if fieldname == 'year':
				ref_doc['year'] = int(value)
			elif fieldname == 'doi':
				doiPrepender = 'http://dx.doi.org/'
				if not rawvalue.startswith("http://"):
					rawvalue = doiPrepender + rawvalue
					ref_doc['url'] = rawvalue
			elif fieldname == 'url':
				ref_doc['url'] = rawvalue
			else:
				ref_doc[fieldname] = value

		authorsAsText = ""
		count = 0
		if bib_data.entries[key].persons:
			numberOfAuthors = len(bib_data.entries[key].persons['author'])
			for person in bib_data.entries[key].persons['author']:

				first = person.get_part_as_text('first')
				last = person.get_part_as_text('last')

				simpleAuthor = bibtex_purify(first + ' ' + last)
				if 'emph' in simpleAuthor:
					simpleAuthor = simpleAuthor.replace('emph', '')

				authorsAsText += simpleAuthor

				if numberOfAuthors > 1:
					if count != (numberOfAuthors - 1):
						authorsAsText += ', '
					if count == (numberOfAuthors - 2):
						authorsAsText += ' and '

				count += 1

		ref_doc['authorsAsText'] = authorsAsText

	except Exception, e:
		print "**** BIBTEX PARSING SCREWED UP ****"
		print e

	return ref_doc

def bibtex_edit(filename, tax_id, ref_doc):
	parser = bib_in.Parser()
	bib_data = parser.parse_file(filename)
	writer = bib_out.Writer(encoding='ascii')

	assert len(bib_data.entries.keys()) == 1

	firstEntry = bib_data.entries.keys()[0]
	ref_doc = set_ref_from_entry(firstEntry, bib_data, ref_doc)

	ReferenceFamily(tax_id).save_reference(ref_doc)

def bibtex_import(filename, taxonomyItem):
	family = ReferenceFamily(taxonomyItem.int_pk())
	parser = bib_in.Parser()
	bib_data = parser.parse_file(filename)

	for key in bib_data.entries.keys():
		ref_doc = ReferenceGlobal().create_reference(taxonomyItem.id)
		ref_doc = set_ref_from_entry(key, bib_data, ref_doc)

		new_ref_id = family.add_reference(ref_doc)
		recent_references.add_reference(ref_doc, new_ref_id, taxonomyItem.int_pk())

	print "Imported %i BibTeX references." % len(bib_data.entries)
