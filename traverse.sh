#!/bin/bash
id=0;
for I in */; do 
	echo $id\|$I >> myitems.csv;
	for X in "$I"*; do
		echo \|\|$id\|$X\|\| >> myfiles.csv;
	done
	let id=id+1;
done
