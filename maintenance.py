
import web.reference_import_couch
from web.models import TaxonomyItem
from web.reference_import_couch import rescan_bibtex

"""
	rebuilds the attributes of each reference object in the database given its bibtex attribute.
	useful for extracting and storing additional metadata from the bibtex parsing code
"""
def rescan_all_references():
	print "Rescanning all references in system."
	count = 0
	for taxonomy in TaxonomyItem.objects.all():
		for ref in taxonomy.references(): 
			rescan_bibtex(taxonomy.id,ref[0])
				
		count += 1

	print "Rescanned %i references." % count
