
"""
 Script used for BibTeX file importing into database from terminal
 Usage - bibtex_import.py -f /path/to/bibtex
 Really not bulletproof but it'll do for now.
"""

from optparse import OptionParser
from web.models import Reference

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="input filename", metavar="FILE")

(options, args) = parser.parse_args()

try:
	f = open(options.filename)
	lines = f.readlines()
except:
	print "Couldn't open file " + options.filename

print "Reading from bibtex file... " + options.filename

i = 0
while i < len(lines):
	if lines[i][0] == '@':
		entry_begin = i

		# let's pull the next line in incase of line breaks in the preamble 
		preamble = lines[i] + lines[i+1] + lines[i+2]
		entry_id = preamble.partition('{')[2].partition(',')[0]
		# sanity/debug: print the extracted entryID
		print entry_id

		# now grab the remainder
		remainder = ""
		bracket_depth = 0
		had_bracket = False
		i = entry_begin
		
		# traverse each line for brackets, keeping track of bracket depth
		# terminate when bracket depth is zero again
		while (not (had_bracket and bracket_depth == 0)) and i < len(lines):
			line = lines[i]
			c = 0
			while c < len(line):
				# skip escapes!
				if line[c] == '\\':
					c += 1
				elif line[c] == '{':
					had_bracket = True
					bracket_depth += 1
				elif line[c] == '}':
					bracket_depth -= 1
				c += 1
			
			remainder += line
			i = i + 1
	
		# destroy ref if already existing
		try:
			existing = Reference.objects.get(entry_id = entry_id)
			existing.delete()
		except:
			None
	
		# save
		# save into DB through Model
		Reference(entry_id = entry_id.decode('utf-8'), bibtex = remainder.decode('utf-8')).save()	
	else:
		i += 1		
	

