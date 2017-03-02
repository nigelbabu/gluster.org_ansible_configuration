#!/bin/bash
# lancer aide
(echo "Start of the run " ; date -u) >> /var/log/aide_scan.log
if [ -f /srv/aidedb.gz ]; then
    /sbin/aide -c /etc/aide_mirror.conf -i
    cp -f /srv/aidedb.new.gz /srv/aidedb.gz
else
    /sbin/aide -c /etc/aide_mirror.conf -u >> /var/log/aide_scan.log 2>&1
    cp -f /srv/aidedb.new.gz /srv/aidedb.gz
fi;
(echo "End of the run " ; date -u) >> /var/log/aide_scan.log
