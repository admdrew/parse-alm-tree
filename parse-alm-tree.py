#!/usr/bin/env python

import sys
import re
from bs4 import BeautifulSoup

# usage: parse-alm-tree.py [path]
# "Subject\Mobility\WorkSite iOS\Search"
# path: partial path to display, ie:
# parse-alm-tree.py "MFP Connector" -> returns all MFP TCs
# parse-alm-tree.py "Mobility\WorkSite iOS" -> returns all iOS TCs
# parse-alm-tree.py "Mobility\WorkSite iOS\Search" -> returns TCs under Search (ie Email, Folders, Save Search, etc)
path_str = "Subject"
if len(sys.argv) > 1:
	path_str += "\\" + sys.argv[1]
path_re_str = re.sub(r"\\", r"/", path_str)
#print(path_re_str)
path_re = re.compile(path_re_str)

soup = BeautifulSoup(open("subject-tree-report.html"))

# defaults/constants
SUBJECT = ""
TEST_NAME = ""
PRODUCT = "MFP"
PRIORITY = ""
DESCRIPTION = ""
STEP_NAME = ""
STEP_DESC = ""
STEP_EXPECT = ""
STATUS = "Review"
OWNER = ""

# m = p.match( 'string goes here' )
# if m:
    # print 'Match found: ', m.group()
# else:
    # print 'No match'
# re.match(pattern, string, flags=0)

# Parent hierarchy starting with h3 tag
# 1, td, child rows: 0
# 2, tr, child rows: 0
# 3, tbody, child rows: 1
# 4, table, child rows: 0 - contains either folder name or list of TCs
# 5, td, child rows: 0
# 6, tr, child rows: 0
# 7, table, child rows: 2 - contains either 2 (no child TCs) or 3 (has child TCs) child rows
# td, child rows: 0
# tr, child rows: 0
# table, child rows: 54
# td, child rows: 0
# center, child rows: 0
# table, child rows: 0
# body, child rows: 0
# html, child rows: 0
# [document], child rows: 0

#print(soup.prettify())

#for header in soup.find_all('h3'):
#  tc_path_str = header.string
  #print(tc_path_str)
  
  #print(header.parent.parent.parent.parent.parent.name)
  
# FIRST header
header = soup.find('h3')
# ALL headers
headers = soup.find_all('h3')
# tc_path_str = header.string
# print(tc_path_str)
# folder_table = header.parent.parent.parent.parent.parent.parent.parent
# for row in folder_table.find_all('tr', recursive=False):
	# print("cells: " + str(len(list(row.find_all('td', recursive=False)))))

#print(str(len(headers)))

# for parent in header.parents:
	# if parent is None:
		# print(parent)
	# else:
		# #print(parent.name + " " + str(len(list(parent.children))))
		# print(parent.name + ", child rows: " + str(len(list(parent.find_all('tr', recursive=False)))))

# !! iterate through each folder_table, containing 2 or 3 rows:
# 0 - folder name
# 1 - empty??
# 2 - (optional) list of TCs
for header in headers:
	folder_table = header.parent.parent.parent.parent.parent.parent.parent # I... I know. 7 parents up
	child_rows = folder_table.find_all('tr', recursive=False) # get only direct children
	name_row = child_rows[0]
	tc_rows = None # possible list of rows containing TCs
	
	if len(child_rows) == 3:
		tc_rows = child_rows[2].td.table.find_all('tr', recursive=False)
	
	#print folder_table.name
	#print("rows: " + str(len(child_rows)))
	folder_name = name_row.td.table.tbody.tr.td.h3.string
	#print(folder_name)
	folder_name_temp = re.sub(r"\\", r"/", folder_name)
	folder_match = path_re.match(folder_name_temp)
	#print("found " + path_str + " in " + folder_name + "?: " + str(folder_match))
	# for row in child_rows:
		# print("cells: " + str(len(list(row.find_all('td', recursive=False)))))
	
	if tc_rows is not None and folder_match:
		#print(folder_name)
		SUBJECT = re.sub(r"Subject\\", "", folder_name) # kill off "Subject\" in path
		#print("tc_row children: " + str(len(list(tc_row.find_all('tr', recursive=False)))))
		for i in range(1, len(tc_rows)):
			tc_cells = tc_rows[i].find_all('td', recursive=False)
			
			# if a description is set for a TC, tc_cells[0] will contain a table with description info
			# so, if not None, we can output everything here
			if tc_cells[0].string is not None:
				TEST_NAME = tc_cells[0].string
				owner_raw = tc_cells[2].string
				OWNER = re.split(" ", owner_raw)[0]	# kill off full name output
				
				output_csv = ""
				output_csv += SUBJECT + ","
				output_csv += TEST_NAME + ","
				output_csv += PRODUCT + ","
				output_csv += PRIORITY + ","
				output_csv += DESCRIPTION + ","
				output_csv += STEP_NAME + ","
				output_csv += STEP_DESC + ","
				output_csv += STEP_EXPECT + ","
				output_csv += STATUS + ","
				output_csv += OWNER
				
				print(output_csv)
		
	# else:
		# print("no children")
	
	#print(" ")