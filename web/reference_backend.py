import web.models
from pybtex.bibtex.utils import bibtex_purify

sortable_attributes = ['year', 'journal', 'title', 'authors']


def format_name(person):
    def join(l):
        return ' '.join([name for name in l if name])

    first = bibtex_purify(person.first_name)
    middle = bibtex_purify(person.middle_name)
    prelast = bibtex_purify(person.prelast_name)
    last = bibtex_purify(person.last_name)
    s = ''
    if last:
        s += join([prelast, last])
        s += ", "
    if first or middle:
        s += first[0:1] + "."
    return s


def getFormattedAuthorList(authors):
    authorsAsString = ""
    count = 0
    numberOfAuthors = len(authors.all())
    for author in authors.all():

        authorsAsString += format_name(author)

        if count != numberOfAuthors - 1:
            authorsAsString += ", "
        if count == numberOfAuthors - 2:
            authorsAsString += " and "
        count += 1
    return authorsAsString


class SortableReference():
    def __init__(self, ref):

        # copy attributes over
        self.bibtex = ref.bibtex
        self.entry_key = ref.entry_key
        self.authors = getFormattedAuthorList(ref.authors)
        self.title = ref.title
        self.journal = ref.journal
        self.year = ref.year

        # get list of attribute objects for reference
        self.attrs = dict()
        for attr_name in sortable_attributes:
            if 'title' in attr_name:
                self.attrs[attr_name] = self.title
            elif 'journal' in attr_name:
                self.attrs[attr_name] = self.journal
            elif 'year' in attr_name:
                self.attrs[attr_name] = self.year
            elif 'authors' in attr_name:
                self.attrs[attr_name] = self.authors


def sorted_reference_list(request, existing_list=None):
    def sort_by_attr(attr_name, default_value):
        return sorted(sortable,
                      key=lambda x: x.attrs[attr_name] if x.attrs[attr_name] is not None else default_value)

    try:
        sort_attr = request.GET['sort']
    except:
        sort_attr = None

    print sort_attr
    if existing_list is None:
        existing_list = web.models.Reference.objects.all()

    sortable = [SortableReference(x) for x in existing_list]

    return sortable if sort_attr is None else sort_by_attr(sort_attr, 0)