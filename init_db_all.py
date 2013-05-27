"""
 Initialises a decent databsae for testing purposes
 Be sure DJANGO_SETTINGS_MODULE='viscommunityweb.settings' in your env settings before running
"""

import os
from django.contrib.auth.models import User
from web.models import TaxonomyItem
import random

db_file = os.path.join(os.getcwd(), 'visweb.db')

# delete existing database file
if os.path.exists(db_file):
    answer = raw_input('Are you sure you want to delete existing visweb.db? [y/n]')
    if answer.lower() == 'y':
        os.remove(db_file)

# run syncdb to generate new one
os.system('python ' + os.path.join(os.getcwd(), 'manage.py syncdb'))
#call_command('syncdb')

# setup references and taxonomy items
from taxonomy_init import taxonomy_init

# bibtex_import(bibtex_file)
taxonomy_init()