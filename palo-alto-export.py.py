#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  palo-alto-export.py
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

import xml.etree.ElementTree as ET
import csv

def find_text(_text,_in_xml):
	_temp = ""
	for all_temp in _in_xml.findall('.//' + _text + '/member'):
		if _temp == "":
			_temp = all_temp.text
		else:
			_temp = _temp + "; " + all_temp.text
	return _temp

def main(args):
	_filename = sys.argv[1]+'.csv'
	tree = ET.parse(sys.argv[1])

    # open a file for writing
	config_data = open(_filename, 'w')
    # create the csv writer object
	csvwriter = csv.writer(config_data)

	_rule_header = ['name','from','to','source', 'NOT', 'destination','user','category','app','service','hip','action','disabled']
	csvwriter.writerow(_rule_header)

	for node in tree.findall('.//devices/entry'):
		name = node.get('name')
		if name == "localhost.localdomain":
			for node2 in node.findall('.//vsys/entry'):
				name2 = node2.get('name')
				if name2 == "vsys1":
					for rule_entry in node2.findall('.//rulebase/security/rules/entry'):
						rule_content = []
						rule_content.append(rule_entry.get('name'))
						rule_content.append(find_text("from",rule_entry))
						rule_content.append(find_text("to",rule_entry))
						rule_content.append(find_text("source",rule_entry))				
						negate_dest = rule_entry.find('.//negate-destination')
						if negate_dest is not None:
							rule_content.append(rule_entry.find('.//negate-destination').text)
						else:
							rule_content.append('')
						rule_content.append(find_text("destination",rule_entry))
						rule_content.append(find_text("source-user",rule_entry))	
						rule_content.append(find_text("category",rule_entry))
						rule_content.append(find_text("application",rule_entry))
						rule_content.append(find_text("service",rule_entry))				
						rule_content.append(find_text("hip-profiles",rule_entry))
						rule_content.append(rule_entry.find('.//action').text)
						disabled = rule_entry.find('.//disabled')
						if disabled is not None:
							rule_content.append(rule_entry.find('.//disabled').text)
						csvwriter.writerow(rule_content)
	config_data.close()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

