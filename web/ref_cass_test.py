import logging
from pybtex.bibtex.utils import bibtex_purify
from pybtex.database.input import bibtex as bib_in
from pybtex.database.output import bibtex as bib_out
from reference_cassandra import *
import StringIO

logger = logging.getLogger(__name__)

def getTitle(fields):
    titleAliases = ['title', 'Title']

    for alias in titleAliases:
        if fields[alias]:
            return bibtex_purify(fields[alias])

def bibtex_import(filename):
	tax_guid = "FIUHIUHF"
	family = ReferenceFamily(tax_guid)
	parser = bib_in.Parser()
	bib_data = parser.parse_file(filename)
	writer = bib_out.Writer(encoding='ascii')

	for key in bib_data.entries.keys():
		stream = StringIO.StringIO()
		writer.write_entry(key, bib_data.entries[key], stream)
		title = getTitle(bib_data.entries[key].fields)
		print "Creating ref " + key + ", " + title
		ref_obj = Reference.get_create_on_key_title(key, title)
		print ref_obj
		ref_obj.bibtex = stream.getvalue()

		try:
			ref_obj.save()

			for field in bib_data.entries[key].fields:
				value = bib_data.entries[key].fields[field]
				col = get_column(field)

				if 'title' in field.lower():
					ref_obj.title = title
				elif 'journal' in field.lower():
					ref_obj.journal = bibtex_purify(value)
				elif 'year' in field.lower():
					ref_obj.year = int(value)
				elif 'url' in field.lower():
					ref_obj.url = value
				elif 'abstract' in field.lower():
					ref_obj.abstract = value
				elif 'doi' in field.lower():
					doiPrepender = 'http://dx.doi.org/'
					if not value.startswith(doiPrepender):
						value = doiPrepender + value
					ref_obj.url = value

				#attr = ReferenceAttribute(ref_obj, col, value)
				#attr.save()

			authorsAsText = ""
			count = 0
			if bib_data.entries[key].persons:
				numberOfAuthors = len(bib_data.entries[key].persons['author'])
				for person in bib_data.entries[key].persons['author']:

					first = person.get_part_as_text('first')
					middle = person.get_part_as_text('middle')
					prelast = person.get_part_as_text('prelast')
					last = person.get_part_as_text('last')
					lineage = person.get_part_as_text('lineage')

					simpleAuthor = bibtex_purify(first + ' ' + last)
					if 'emph' in simpleAuthor:
						simpleAuthor = simpleAuthor.replace('emph', '')

					authorsAsText += simpleAuthor

					if numberOfAuthors > 1:
						if count != (numberOfAuthors -1):
							authorsAsText += ', '
						if count == (numberOfAuthors - 2):
							authorsAsText += ' and '

					count += 1


			ref_obj.authorsAsText = authorsAsText
			ref_obj.save()

		except Exception, e:
			logger.log(e.message)
			connection._rollback()

	print "Imported %i BibTeX references." % len(bib_data.entries)
	print "This taxon now has items:"
	items = family.all_refs()
	for item in items:
		print item


bibtex_import("/Users/sim/Desktop/testone.bib")
