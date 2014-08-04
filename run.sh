#!/bin/sh
base="line"
linethrift="$base/linethrift"
if [ -d "$linethrift" ]; then
    echo "$linethrift already exists"
    rm -rf $linethrift
    mkdir $linethrift
else
    mkdir $linethrift
fi

thrift -out $linethrift --gen py:new_style $base/line.thrift

rm $linethrift/__init__.py
mv $linethrift/linethrift/*.py $linethrift
rm -rf $linethrift/linethrift
