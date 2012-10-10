
"""
 Initialises a decent databsae for testing purposes
 Be sure DJANGO_SETTINGS_MODULE='viscommunityweb.settings' in your env settings before running
"""

import os
from django.contrib.auth.models import User
from web.models import TaxonomyItem
import random

db_file = os.path.join(os.getcwd(),'visweb.db')
bibtex_file = os.path.join(os.getcwd(),'bibtex','test.bib')

# delete existing database file
if os.path.exists(db_file):
	answer = raw_input('Are you sure you want to delete existing visweb.db? [y/n]')
	if answer.lower() == 'y':
		os.remove(db_file)

# run syncdb to generate new one
os.system('python ' + os.path.join(os.getcwd(),'manage.py syncdb'))

# setup references and taxonomy items
from taxonomy_init import taxonomy_init
from bibtex_import_server import bibtex_import

bibtex_import(bibtex_file)
taxonomy_init()

# add some users
for i in range(10):
	user = User.objects.create_user('TestUser' + str(i) + "@gmail.com", 'TestUser' + str(i) +'@gmail.com', 'password')
	user.save()

# set up some ownership for taxonomy items
for user in User.objects.all():
	for tax_item in TaxonomyItem.objects.all():
		if random.random() < 0.05:
			tax_item.owners.add(user)
