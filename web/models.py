"""
 Data models
"""
from collections import defaultdict
from django.contrib.auth.models import User
from django.db import models
import user
import uuid
import hashlib
from datetime import datetime
from couchdb import *
import json

server = Server("http://127.0.0.1:5984/")


class TaxonomyArea(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class TaxonomyCategory(models.Model):
    name = models.CharField(max_length=128)
    area = models.ForeignKey(TaxonomyArea, null=True, blank=True)

    parent = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name


class TaxonomyItem(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(TaxonomyCategory)
    detail = models.TextField(default="")
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(User, null=True)
    owners = models.ManyToManyField(User, related_name="owners+")

    def int_pk(self):
        try:
            return self.pk[0]
        except:
            return self.pk

    def reference_family(self):
        return ReferenceFamily(self.int_pk())

    def references(self, sort=None):
        return ReferenceFamily(self.int_pk()).get_references(sort)

    def remove_reference(self, ref_id):
        ReferenceFamily(self.int_pk()).remove_reference(ref_id)

    def short_description(self):
        return self.detail[:50] + '...'

    def __unicode__(self):
        return self.name + " (" + self.category.name + ")"


# represents a reference (duh)
class Reference(object):
    def __init__(self):
        self.id = '' # duplicate of Couch's _id, but Django's template system doesn't like underscores
        self.entry_key = ''
        self.title = ''
        self.bibtex = ''
        self.year = ''
        self.authorsAsText = ''
        self.abstract = ''
        self.journal = ''
        self.year = 0
        self.url = ''
        self.date_added = str(datetime.now())

    def __unicode__(self):
        return self.entry_key + ", " + self.title + " by " + self.authorsAsText + " in year " + str(self.year)

# reference Family - one per TaxonomyItem (as identified by its id)
class ReferenceFamily(object):
    # initialise a reference family for a taxonomy id
    def __init__(self, tax_id):
        self.db = None
        self.tax_id = str(tax_id)
        self._ensure_exists()

    # name of this database object
    def database_id(self):
        return "ref_fam_%s" % self.tax_id

    def copy_reference(self, ref_id):
        new_id = uuid.uuid4().hex
        new_rev = self.db.copy(ref_id, new_id)
        return new_id

    def move_all_references(self, new_family):
        for ref_id, rec_doc in self.get_references():
            self.move_reference(ref_id, new_family)

    def move_reference(self, ref_id, new_family):
        new_family.add_reference(self.db[ref_id])
        self.db.purge([self.db[ref_id]])

    # add a reference to this reference family
    def add_reference(self, ref):
        ref = ref.__dict__ if type(ref) is Reference else ref
        doc_id, rev_id = self.db.save(ref)
        # Django doesn't like Couch's _id so we'll create a redundant id attribute
        doc = self.db[doc_id]
        doc['id'] = doc_id
        self.db.save(doc)
        return doc_id

    # get a reference by id
    def get_reference(self, ref_id):
        return self.db[ref_id]

    def delete_reference(self, ref_id):
        return self.db.delete(self.db[ref_id])

    # get all references
    def get_references(self, sort=None):
        emit = "emit(d._id,d)"
        if sort is not None:
            emit = "emit(d.%s,d)" % sort

        return [(x.key, x.value) for x in self.db.query("function(d) { " + emit + "; }")]

    def get_references_as_dict(self, sort=None):
        refs = self.get_references()
        d = defaultdict(list)
        for k, v in refs:
            d[k] = v
        return d.items()

    # remove a reference by id
    def remove_reference(self, ref_id):
        self.db.delete(self.get_reference(ref_id))

    def remove_all_references(self):
        all_refs = self.get_references()
        for k, v in all_refs:
            self.delete_reference(k)

    # ensures db object exists; creates if not
    def _ensure_exists(self):
        try:
            self.db = server[self.database_id()]
        except:
            print "Creating database %s" % self.database_id()
            self.db = server.create(self.database_id())
            self.db.commit()
        assert (self.db is not None)

# functions for dealing with references without worrying about which taxonomy they're attached to (ehh...)
class ReferenceGlobal(object):
    def __init__(self):
        self.all_tax_ids = [x.id for x in list(TaxonomyItem.objects.all())]

    def get_reference(self, tax_id, ref_id):
        return ReferenceFamily(tax_id).get_reference(ref_id)

    def remove_reference(self, tax_id, ref_id):
        return ReferenceFamily(tax_id).remove_reference(ref_id)

    def tax_items_featuring_ref(self, ref_id):
        tax_ids = []
        for tax_id in self.all_tax_ids:
            try:
                tax_ids.append(ReferenceFamily(tax_id).get_reference(ref_id))
            except:
                pass
        return tax_ids

# represents a fixed-size queue of recent reference entries
class ReferenceQueue(ReferenceFamily):
    def __init__(self, size):
        super(ReferenceQueue, self).__init__(0)
        self.queue_size = size

    def database_id(self):
        return "ref_recent"

    def add_reference(self, ref, ref_id, tax_id):
        ref.ref_doc_id = ref_id
        ref.tax_id = tax_id
        super(ReferenceQueue, self).add_reference(ref)
        self.limit_queue()

    def limit_queue(self):
        docs = self.db.query("function(d) { emit(d.id); }", descending=True, skip=self.queue_size)
        for item in docs:
            print item
            self.db.delete(self.db[item.id])


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    orcid = models.CharField(max_length=19, blank=True)
    gravatarEmail = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return user

    def get_absolute_url(self):
        return 'profiles_profile_detail', (), {'username': self.user.username}

    get_absolute_url = models.permalink(get_absolute_url)


class OwnershipRequest(models.Model):
    requester = models.ForeignKey(User)
    taxonomyItem = models.ForeignKey(TaxonomyItem)
    additionalNotes = models.TextField()

    def __unicode__(self):
        return self.requester.username + ' - ' + self.taxonomyItem.name


class Enquiry(models.Model):
    requester = models.ForeignKey(User)
    taxonomyItem = models.ForeignKey(TaxonomyItem)
    enquiry_type = models.CharField(max_length=256, default="")
    # optional
    #reference = models.ForeignKey(Reference, null=True)
    additionalNotes = models.TextField()

# front page recent references
recent_references = ReferenceQueue(3)

