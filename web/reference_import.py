import logging
from pybtex.bibtex.utils import bibtex_purify
from pybtex.database.input import bibtex as bib_in
from pybtex.database.output import bibtex as bib_out
from web.models import Reference, ReferenceColumn, ReferenceAttribute, ReferenceAuthor
import StringIO

logger = logging.getLogger(__name__)


def generate_nonduplicate_key(ref_key):
    rk = ref_key + str(1)
    i = 1
    while True:
        try:
            Reference.objects.get(rk)
        except:
            return rk
        else:
            i += 1
            rk = ref_key + str(i)


def get_ref(ref_key, title, bibtex):
    ref, created = Reference.objects.get_or_create(title=title)
    if not created:
        ref_key = generate_nonduplicate_key(ref_key)
        ref.entry_key = ref_key
    ref.bibtex = bibtex
    return ref


def get_column(column_name):
    col = None
    try:
        col = ReferenceColumn.objects.get(name=column_name)
    except:
        col = ReferenceColumn(name=column_name)
        col.save()
    return col


def getTitle(fields):
    titleAliases = ['title', 'Title']

    for alias in titleAliases:
        if fields[alias]:
            return bibtex_purify(fields[alias])


def bibtex_import(filename, taxonomyItem):
    parser = bib_in.Parser()
    bib_data = parser.parse_file(filename)
    writer = bib_out.Writer(encoding='ascii')

    for key in bib_data.entries.keys():

        stream = StringIO.StringIO()
        writer.write_entry(key, bib_data.entries[key], stream)

        title = getTitle(bib_data.entries[key].fields)

        ref_obj = get_ref(key, title, stream.getvalue())
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
            elif 'url' in field.lower() or 'doi' in field.lower():
                ref_obj.url = value
            elif 'doi' in field.lower():
                doiPrepender = 'http://dx.doi.org/'
                if not value.startswith(doiPrepender):
                    value = doiPrepender + value
                ref_obj.url = value

            attr = ReferenceAttribute(column=col, value=value)
            attr.save()

            ref_obj.referenceAttributes.add(attr)
        if bib_data.entries[key].persons:
            for person in bib_data.entries[key].persons['author']:
                first = person.get_part_as_text('first')
                middle = person.get_part_as_text('middle')
                prelast = person.get_part_as_text('prelast')
                last = person.get_part_as_text('last')
                lineage = person.get_part_as_text('lineage')

                try:
                    author, created = ReferenceAuthor.objects.get_or_create(first_name=first, last_name=last)
                except Exception, e:
                    logger.debug('Author ' + first + ' ' + last + ' exists in multiple places. Error is ' + e.message)
                    author = ReferenceAuthor.objects.filter(first_name=first).filter(last_name=last).__getitem__(0)
                    created = False

                if created:
                    author.middle_name = middle
                    author.prelast_name = prelast
                    author.lineage = lineage
                    author.save()

                if not author in ref_obj.authors.all():
                    ref_obj.authors.add(author)

        ref_obj.save()
        if not ref_obj in taxonomyItem.references.all():
            taxonomyItem.references.add(ref_obj)

    print "Imported %i BibTeX references." % len(bib_data.entries)