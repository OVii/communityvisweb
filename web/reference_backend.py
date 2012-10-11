
import web.models
from pybtex.bibtex.utils import bibtex_purify

sortable_attributes = ['year','journal','title','booktitle','issn']

class SortableReference():
	"""
	 returns a reference object with new python attributes pulled from the reference_attributes link;
	 useful for sorting
	"""
	def html(self):
		def attribute_html(attr_name):
			try:
				return '<span class="reference_%s">%s</span>' % (attr_name, self.attrs[attr_name].value)
			except:
				return ''

		html_str = '<div class="reference_box">'

		html_str += '<span class="reference_authors">'
		html_str += ' and '.join([format_name(person) for person in self.authors.all()])
		html_str += '</span>'

		attributes = ['year','title']
		html_str += ''.join([ attribute_html(x) for x in self.attrs ])

		html_str += '</div>'

		return html_str

	def __init__(self, ref):
		def attribute(attr_name):
			try:
				return web.models.ReferenceAttribute.objects.get(column__name__exact=attr_name,reference=ref)
			except:
				return None

		# copy attributes over	
		self.bibtex = ref.bibtex
		self.entry_key = ref.entry_key
		self.authors = ref.authors

		# get list of attribute objects for reference
		self.attrs = dict()
		for attr_name in sortable_attributes:
			self.attrs[attr_name] = attribute(attr_name)

def sorted_reference_list(request, existing_list = None):
	def sort_by_attr(attr_name, default_value):
		return sorted(sortable, key=lambda x: x.attrs[attr_name].value if x.attrs[attr_name] is not None else default_value)

	try:
		sort_attr = request.GET['sort']
	except:
		sort_attr = None

	if existing_list is None:
		existing_list = web.models.Reference.objects.all()
 
	sortable = [ SortableReference(x) for x in existing_list ]

	return sortable if sort_attr is None else sort_by_attr(sort_attr,0)

def format_name(person):
	def join(l):
		return ' '.join([name for name in l if name])
	first = bibtex_purify(person.first_name)
	middle = bibtex_purify(person.middle_name)
	prelast = bibtex_purify(person.prelast_name)
	last = bibtex_purify(person.last_name)
	lineage = bibtex_purify(person.lineage)
	s = '' 
	if last:
		s += join([prelast, last])
	if lineage:
		s += ', %s' % lineage
	if first or middle:
		s += ', '
		s += join([first, middle])
	return s

		
"""
$("body").append("<div class=\"bibtex_template\"> <div class=\"if author\" style=\"font-weight: bold;\">\n  " +
                "<span class=\"ref_begin\"></span> <span class=\"if year\">\n    " +
                "<span class=\"year\"></span>, \n  </span>\n  " +
                "<span class=\"author\"></span>\n  <span class=\"if url\" " +
                "style=\"margin-left: 20px\">\n    " +
                "<a class=\"btn btn-small\" style=\"color:black; font-size:10px\"><i class=\"icon-book\"></i> View Online</a>\n  </span>\n</div>" +
                "<div style=\"margin-left: 10px; margin-bottom:5px;\">\n  " +
                "<span class=\"title\"></span>\n</div></div>");
"""
