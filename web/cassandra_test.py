
from reference_cassandra import *

fam = ReferenceFamily("testy")
fam.add("test bibtex")
print fam.all_refs()
