#!/bin/bash

src="../processed/"
dest1="processed_learning/"
dest2="processed_test/"

mkdir -p $dest1
mkdir -p $dest2

for file in $( ls $src); do
    i=$((${#file}-5))
    lastdigit=${file:$i:1}
    if(("$lastdigit" < "7")); then
        cp $src$file $dest1
    else
        cp $src$file $dest2
    fi
done














