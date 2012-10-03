
"""
 Initialises a decent databsae for testing purposes
 Be sure DJANGO_SETTINGS_MODULE='viscommunityweb.settings' in your env settings before running
"""

import os

db_file = os.path.join(os.getcwd(),'visweb.db')
bibtex_file = os.path.join(os.getcwd(),'bibtex','test.bib')

if os.path.exists(db_file):
	answer = raw_input('Are you sure you want to delete existing visweb.db? [y/n]')
	if answer.lower() == 'y':
		os.remove(db_file)

os.system('python ' + os.path.join(os.getcwd(),'manage.py syncdb'))

from taxonomy_init import taxonomy_init
from bibtex_import import bibtex_import

bibtex_import(open(bibtex_file))
taxonomy_init()


