#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  juniper-srx-rulebase-convert.py
#  
#  Copyright 2017 Dieter Sarrazyn <dieter[at]secudea[dot]be>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import csv

def main(args):
	_filename = sys.argv[1]+'.csv'

    # open a file for writing
	config_data = open(_filename, 'w')
    # create the csv writer object
	csvwriter = csv.writer(config_data)

	_rule_header = ['name','from','to','source','destination','user','category','app','service','hip','action','disabled']
	csvwriter.writerow(_rule_header)

	rule_start = None
	rule_name = ''
	rule_from = ''
	rule_to = ''
	rule_app = ''
	rule_service = ''
	rule_action = ''
	rule_match_section = None
	rule_action_section = None
	zone_start = None
	zone_from = ''
	zone_to = ''
	policies_start = None
	

	with open(sys.argv[1]) as f:
		for line in f:
			if line[4:12] == 'policies':
				policies_start = True
			if line[4:9] == 'zones':
				policies_start = False
			if policies_start:
				splitted_line = line.split()
				if line[8:17] == 'from-zone':
					zone_start = True
					zone_from = splitted_line[1]
					zone_to = splitted_line[3]
				if line[12:18] == 'policy':
					rule_start = True
					rule_name = splitted_line[1]
				if rule_start:
					if line[16:21] == 'match':
						rule_match_section = True
						rule_action_section = False
					if rule_match_section:
						if splitted_line[0] == 'source-address':
							try: rule_from = line[line.index('[')+2:line.index(']')-1].replace(' ',';')
							except: rule_from = splitted_line[1].rstrip('\;')
						if splitted_line[0] == 'destination-address':
							try: rule_to = line[line.index('[')+2:line.index(']')-1].replace(' ',';')
							except: rule_to = splitted_line[1].rstrip('\;')
						if splitted_line[0] == 'application':
							try: rule_app = line[line.index('[')+2:line.index(']')-1].replace(' ',';')
							except: rule_app = splitted_line[1].rstrip('\;')
													
					if rule_action_section:
						rule_action = splitted_line[0]
						rule_action_section = False
					if line[16:20] == 'then':
						rule_action_section = True
						rule_match_section = False						
					
				if line[12:13] == '}':
					rule_start = False
					rule_content = []
					rule_content.append(rule_name)
					rule_content.append(zone_from)
					rule_content.append(zone_to)
					rule_content.append(rule_from)				
					rule_content.append(rule_to)	
					rule_content.append('') #user
					rule_content.append('') #category
					rule_content.append(rule_app)
					rule_content.append(rule_service)				
					rule_content.append('') #hip
					rule_content.append(rule_action)
					rule_content.append('') #disabled or not
					csvwriter.writerow(rule_content)
					rule_name = ''
					rule_from = ''
					rule_to = ''
					rule_app = ''
					rule_service = ''
					rule_action = ''

				if line[8:9] == '}':
					zone_start = False
					zone_from = ''
					zone_to = ''
					

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

