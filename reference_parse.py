
"""
 For taxonomy items, we can add references like this {{bibtex_entry_id}}. The defs in this file
 deal with parsing and formatting this text from the database and into the pages.
"""

from web.models import Reference

"""
 Returns a list of tuples denoting the indices of all references (including {{}} brackets)
"""
def indices(meta_str):
	ind = []
	i = 0
	while i < len(meta_str):
		if meta_str[i] == '{' and meta_str[i+1] == '{':
			'skip ahead to end bracket'
			start = i
			while meta_str[i] != '}' and i < len(meta_str):
				i = i + 1
			
			print "Indices start: " + str(start) + " and i: " + str(i)
			ref_str = meta_str[start:i]
			
			ind = ind + [(start,i+1)]
		else:
			i = i + 1
	return ind

"""
 Returns a list of Reference objects for a given meta string
"""
def reference_entries(meta_str):
	"Use a dictionary to ensure no duplicates"
	refs = dict()

	for (i,j) in indices(meta_str):
		ref = meta_str[i+2:j-1]
		try:
			ref_obj = Reference.objects.get(entry_id=ref)
		except:
			pass
		else:
			refs[ref] = ref_obj

	return refs.values()

"""
 Strips the reference meta tags and replaces with <a href>'s
"""
def html_format(meta_str):
	ind = indices(meta_str)
	ref_idx_dict = dict()
	ref_idx = 1

	if len(ind) == 0:
		return meta_str

	html_str = meta_str[0:ind[0][0]]
	for i in range(len(ind)):
		(a,b) = ind[i]
		ref_id = meta_str[a+2:b-1]
	
		if not ref_idx_dict.has_key(ref_id):
			ref_idx_dict[ref_id] = ref_idx
			ref_idx += 1	

		html_str = html_str + '<span class="badge badge-info">\
			<a href="#' + str(ref_idx_dict[ref_id]) + '" style="color:white">' + str(ref_idx_dict[ref_id]) + '</a></span>'

		if i < len(ind)-1:
			(c,d) = ind[i+1]
			html_str = html_str + meta_str[b+1:c]
		else:
			html_str = html_str + meta_str[b+1:]

	return html_str
