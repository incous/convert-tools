#!/bin/sh

if ([ "$#" -ne 2 ] || ([ "$1" != 'backup' ] && [ "$1" != 'restore' ])); then
	echo "Usage: $0 <backup|restore> tarfile"
elif [ $1 = 'backup' ]; then
	if [ -f $2 ]; then
		echo "File $2 existed. Overwrite? (y/n)"
		read ans
		if [ "$ans" == "n" ]; then
			exit 0
		fi
	fi
	declare -a files=('/path/file1' '/path/file2') # list of files/folders
	for file in "${files[@]}"
	do
		tar -rPvf $2 $file
	done
elif [ $1 = 'restore' ]; then
	if [ ! -f $2 ]; then
		echo "File $2 not found!"
	elif [ ! -r $2 ]; then
		echo "Cannot read $2!"
	else
		tar -xPvf "$2"
	fi
fi
