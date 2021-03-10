#!/usr/bin/env python3

# this program specifically adds short gene names for long ids (from maker) from convertion table in the gff file  

import os,sys

table=sys.argv[1]
gff=sys.argv[2]
pfam = sys.argv[3]

# build a database of convertion table

namemappingtable={}
pfam_ids = set()
with open(table) as tfh, open(gff) as gfh, open(pfam) as pfh:
	
	for line in tfh:
		line=line.strip()
		if line == "":
			continue
		else:
			data=line.split()
			id=data[0]
			value=data[1]
		namemappingtable[id] = value

	# let's get pfam ids
	
	for line in pfh:
		if line.startswith("#"):
			continue
		elif line.strip() == "":
			continue
		else:
			pfam_ids.add(line.strip().split()[0])
	
	# we got the list of pfam ids
		
	# we have built the databases
	# let's open gff file and replace the long names for short names

	for line in gfh:
		line = line.strip()
		if line == "":
			continue
		elif line.startswith("#"):
			print(line)
		else:
			data = line.split("\t")
			if len(data) < 9:
				print(line)
				continue

			attributes = data[-1].split(";")
			add_alias = False
			add_pfamid = False
			for position in range(len(attributes)):
				attribute = attributes[position]
				try:
					valuetoreplace = attribute.split("=")[1].split(":")[0]
				except IndexError as ierr:
					sys.stderr.write(attribute)
					exit(1)
				if valuetoreplace in namemappingtable.keys():
					attribute_after_replace = attribute.replace(valuetoreplace, namemappingtable[valuetoreplace])
					attributes[position] =  attribute_after_replace
					if add_alias == False:
						attributes.append("Alias=" + valuetoreplace)
						add_alias = True
					
					# check if the id is in pfam ids, if yes, add Dbxref attribute
					if add_pfamid ==False and namemappingtable[valuetoreplace] in pfam_ids:
						attributes.append("Dbxref=\"Pfam:" + namemappingtable[valuetoreplace] + "\"")
						add_pfamid = True

			data[-1] = ";".join(attributes)
			print("\t".join(data))
			

exit(0)

