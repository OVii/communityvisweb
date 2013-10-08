import logging
from web.models import *
import StringIO
from pybtex.bibtex.utils import bibtex_purify
from pybtex.database.input import bibtex as bib_in
from pybtex.database.output import bibtex as bib_out

logger = logging.getLogger(__name__)

def set_ref_from_entry(key, bib_data, ref_doc):
	stream = StringIO.StringIO()
	writer = bib_out.Writer(encoding='ascii')
	writer.write_entry(key, bib_data.entries[key], stream)
	ref_doc['bibtex'] = stream.getvalue()

	try:
		for field in bib_data.entries[key].fields:
			value = bib_data.entries[key].fields[field]

			fieldname = field.strip().lower()
			value = bibtex_purify(value)

			if fieldname == 'year':
				ref_doc['year'] = int(value)
			elif fieldname == 'doi':
				doiPrepender = 'http://dx.doi.org/'
				if not value.startswith(doiPrepender):
					value = doiPrepender + value
				ref_doc['url'] = value
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
