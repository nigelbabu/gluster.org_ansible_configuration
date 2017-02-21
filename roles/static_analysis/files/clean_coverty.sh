#!/bin/bash

cd /var/www/html/pub/gluster/glusterfs/static-analysis/
for i in release-* master;
do
    find $i -type f -mtime +45 -exec rm -f {} \; > /dev/null
done
find . -type d -empty -exec rmdir {} \; > /dev/null
