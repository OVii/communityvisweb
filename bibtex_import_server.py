from pybtex.database.input import bibtex as bib_in
from pybtex.database.output import bibtex as bib_out
from optparse import OptionParser
from web.models import Reference, ReferenceColumn, ReferenceAttribute, ReferenceAuthor
import StringIO


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


def get_ref(ref_key, bibtex):
    try:
        existing = Reference.objects.get(entry_key=ref_key)
    except:
        ref_key = generate_nonduplicate_key(ref_key)

    ref = Reference(entry_key=ref_key, bibtex=bibtex)
    ref.save()
    return ref


def get_column(column_name):
    col = None
    try:
        col = ReferenceColumn.objects.get(name=column_name)
    except:
        col = ReferenceColumn(name=column_name)
        col.save()
    return col


def bibtex_import(filename):
    parser = bib_in.Parser()
    bib_data = parser.parse_file(filename)
    writer = bib_out.Writer(encoding='ascii')

    for key in bib_data.entries.keys():

        print 'Key ' + key

        stream = StringIO.StringIO()
        writer.write_entry(key, bib_data.entries[key], stream)

        ref_obj = get_ref(key, stream.getvalue())
        ref_obj.save()

        for field in bib_data.entries[key].fields:
            value = bib_data.entries[key].fields[field]
            col = get_column(field)

            print 'Field is ' + field
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
                auth = ReferenceAuthor(first_name=first,
                                       middle_name=middle,
                                       prelast_name=prelast,
                                       last_name=last,
                                       lineage=lineage)
                auth.save()
                ref_obj.authors.add(auth)

        ref_obj.save()

    print "Imported %i BibTeX references." % len(bib_data.entries)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="input filename", metavar="FILE")

    (options, args) = parser.parse_args()

    try:
        f = open(options.filename)
    except:
        print "Couldn't open BibTeX file."

    bibtex_import(str(options.filename))


