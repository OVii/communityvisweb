
import web.models
from pybtex.bibtex.utils import bibtex_purify

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

def html_format_entry(ref):
	def attribute_html(attr_name):
		try:
			return '<span class="reference_%s">%s</span>' % (attr_name, web.models.ReferenceAttribute.objects.get(column__name__exact=attr_name,reference=ref).value)
		except:
			return ''

	html = '<div class="reference_box">'

	html += '<div class="reference_authors">'
	html += ' and '.join([format_name(person) for person in ref.authors.all()])
	html += '</div>'

	attributes = ['year','title']
	html += ''.join([ attribute_html(x) for x in attributes ])

	html += '</div>'
	return html
		
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
