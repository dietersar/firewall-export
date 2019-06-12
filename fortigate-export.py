#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fortigate-rulebase-export.py
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

def _concat_string_array(_input):
	_to_exclude = ['',' ','\n']
	_output = ''
	print(_input)
	for i in range(1, len(_input)-1):
		if _input[i] not in _to_exclude:
			if _output == '':
				_output = _input[i].strip()
			else:
				_output = _output + ', ' + _input[i].strip()
	return _output

def main(args):
    # open a file for writing
	_filename = sys.argv[1]+'.csv'
	config_data = open(_filename,'w')
    # create the csv writer object
	csvwriter = csv.writer(config_data)
	
	_rule_header = ['nr','name','srcintf','dstintf','srcaddr','dstaddr','schedule','service','action','logtraffic','comments','label']
	csvwriter.writerow(_rule_header)
	
	config_to_check = open(sys.argv[1],'r')
	_fw_rules = 0
	_next_rule = 0
	_rule_content = [''] * 12
	for line in config_to_check.readlines():
		if _fw_rules == 1:
			_line_splitted = line.split(' ')
			_line_splitted_text = line.split('"')
			if _line_splitted[0] == "edit":
				_rule_content[0] = _line_splitted[1].strip()
			elif _line_splitted[0] == "set":
				if _line_splitted[1] == "name":
					_rule_content[1] = _line_splitted_text[1]
				if _line_splitted[1] == "srcintf":
					_rule_content[2] = _line_splitted_text[1]
				if _line_splitted[1] == "dstintf":
					_rule_content[3] = _line_splitted_text[1]
				if _line_splitted[1] == "srcaddr":
					_rule_content[4] = _concat_string_array(_line_splitted_text)
				if _line_splitted[1] == "dstaddr":
					_rule_content[5] = _concat_string_array(_line_splitted_text)
				if _line_splitted[1] == "schedule":
					_rule_content[6] = _line_splitted_text[1]
				if _line_splitted[1] == "service":
					_rule_content[7] = _concat_string_array(_line_splitted_text)
				if _line_splitted[1] == "action":
					_rule_content[8] = _line_splitted[2].strip()					
				if _line_splitted[1] == "logtraffic":
					_rule_content[9] = _line_splitted[2].strip()
				if _line_splitted[1] == "comments":
					_rule_content[10] = _line_splitted_text[1]
#				if _line_splitted[1] == "global-label":
#					_rule_content[11] = _line_splitted_text[1]				
			elif _line_splitted[0] == "next\n":
				csvwriter.writerow(_rule_content)
				_rule_content = [''] * 11
			
			
		if line == "config firewall policy\n":
			_fw_rules = 1
		if line == "end\n":
			_fw_rules = 0
				
	config_to_check.close()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
