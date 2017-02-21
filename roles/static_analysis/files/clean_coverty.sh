#!/bin/bash

cd /var/www/html/pub/gluster/glusterfs/static-analysis/
for i in release-* ;
do
    find $i -type f -mtime +15 -exec rm -f {} \; > /dev/null
done
find master -type f -mtime +10 -exec rm -f {} \; > /dev/null
find . -type d -empty -exec rmdir {} \; > /dev/null
