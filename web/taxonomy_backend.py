from web.models import TaxonomyArea, TaxonomyCategory, TaxonomyItem

"""
 Builds a dictionary (letter[char]) => { item, item } representing the taxonomy in the system
"""

def alphabetic_index():
    idx = dict()
    # categories
    for item in list(TaxonomyItem.objects.all().order_by('name')):
        val = (item.id, item.name, item.category.name, item.detail, item.category.id)
        if idx.has_key(item.name[0]):
            idx[item.name[0]].append(val)
        else:
            idx[item.name[0]] = [val]
    print idx
    return idx
