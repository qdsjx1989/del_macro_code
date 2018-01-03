#!/usr/bin/env python

import sys
import re
#delm.py AAAAA filepath 1/0
	
input_file=sys.argv[2]

fp=open(input_file, "r+")
all_lines=fp.readlines();
file_len=len(all_lines)
file_cursor=0;
need_delete=int(sys.argv[3]);

need_match = "^\s*#ifndef\s%s" % sys.argv[1]

def delete_macro_v2():
	global all_lines
	global file_cursor
	need_delete=1
	other_ifdef_num = 0
	while 1:
		#match_ifdef =  re.match("^#ifdef", all_lines[file_cursor], 0);
		match_if =  re.match("^#if", all_lines[file_cursor], 0);
		match_else = re.match("^#else", all_lines[file_cursor], 0);
		match_elif = re.match("^#elif", all_lines[file_cursor], 0);
		match_end =  re.match("^#endif", all_lines[file_cursor], 0);
		if match_if is not None and need_delete == 0:
			other_ifdef_num = other_ifdef_num + 1
			file_cursor = file_cursor + 1;
			continue
		if match_if is not None and need_delete == 1:
			other_ifdef_num = other_ifdef_num + 1
			all_lines[file_cursor] = ""
			file_cursor = file_cursor + 1;
			continue
		elif match_else is not None and other_ifdef_num != 0 and need_delete == 0:
			file_cursor = file_cursor + 1;
			continue
		elif match_else is not None and other_ifdef_num != 0 and need_delete == 1:
			all_lines[file_cursor] = ""
			file_cursor = file_cursor + 1;
			continue
		elif match_else is not None and other_ifdef_num == 0 and need_delete == 1:
			need_delete = 0
			all_lines[file_cursor] = ""
			file_cursor = file_cursor + 1;
			continue
		elif match_elif is not None and other_ifdef_num != 0 and need_delete == 0:
			file_cursor = file_cursor + 1;
			continue
		elif match_elif is not None and other_ifdef_num != 0 and need_delete == 1:
			all_lines[file_cursor] = ""
			file_cursor = file_cursor + 1;
			continue
		elif match_elif is not None and other_ifdef_num == 0 and need_delete == 1:
			all_lines[file_cursor] = "#ifdef " + all_lines[file_cursor][5:]
			file_cursor = file_cursor + 1;
			need_delete = 0
			return	
		elif match_elif is not None and other_ifdef_num == 0 and need_delete == 0:
			file_cursor = file_cursor + 1;
			continue
		elif match_end is not None and other_ifdef_num == 0: 
			all_lines[file_cursor] = ""
			file_cursor = file_cursor + 1;
			return
		elif match_end is not None and other_ifdef_num != 0 and need_delete == 0:
			other_ifdef_num = other_ifdef_num - 1
			file_cursor = file_cursor + 1;
			continue
		elif match_end is not None and other_ifdef_num != 0 and need_delete == 1:
			other_ifdef_num = other_ifdef_num - 1
			all_lines[file_cursor] = ""
			file_cursor = file_cursor + 1;
			continue
		else:
			if need_delete == 1:
				all_lines[file_cursor] = ""
			file_cursor = file_cursor + 1;

def delete_macro_v3():
	#print("enter delete_macro_v3")
	global all_lines
	global file_cursor
	global need_delete
	while 1:
        #case 1 nest if    
        	match_if=re.match("^\s*#if", all_lines[file_cursor], 0);
                if match_if is not None:
                        if need_delete == 1:
                                all_lines[file_cursor] = "";
                        file_cursor = file_cursor + 1;
                        handle_nest_if();
        #case 2 else
                match_else=re.match("^\s*#else", all_lines[file_cursor], 0);
                if match_else is not None:
                        all_lines[file_cursor] = ""
                        file_cursor = file_cursor + 1;
                        match_else = re.match("^\s*#endif", all_lines[file_cursor], 0);
                        while match_else is None:
                                if need_delete == 0:
                                        all_lines[file_cursor] = ""
                                file_cursor = file_cursor + 1;
                                match_else = re.match("^\s*#endif", all_lines[file_cursor], 0);
                        all_lines[file_cursor] = ""
                        file_cursor = file_cursor + 1;
                        return
                match_endif=re.match("^\s*#endif", all_lines[file_cursor], 0);
                if match_endif is not None:
                        all_lines[file_cursor] = ""
                        file_cursor = file_cursor + 1;
                        return
                if need_delete == 1:
                        all_lines[file_cursor] = ""
                file_cursor = file_cursor + 1;

def handle_nest_if():

	#print("enter handle_nest_if\n")
	global all_lines
	global file_cursor
	global need_delete
	end=re.match("^\s*#endif", all_lines[file_cursor], 0);
	while end is None:
		if need_delete == 1:
		    all_lines[file_cursor] = "";
		file_cursor = file_cursor + 1;
		end=re.match("^\s*#endif", all_lines[file_cursor], 0);

	if need_delete == 1:
		all_lines[file_cursor] = ""
	file_cursor = file_cursor + 1;

while file_cursor < file_len:
	result=re.match(need_match, all_lines[file_cursor], 0);
	#result2=re.match(need_match2, all_lines[file_cursor], 0);
	if result is not None:
		all_lines[file_cursor] = ""
		file_cursor = file_cursor + 1;
		delete_macro_v3();
	else:
		file_cursor = file_cursor + 1;

fp.seek(0,0)
fp.truncate()
fp.writelines(all_lines)
fp.close()
