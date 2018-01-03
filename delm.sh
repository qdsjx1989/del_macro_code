#!/bin/bash
find . -name "*.c" >dstfile

while read line
do
	delm.py $1 $line
done < dstfile

rm -f dstfile
