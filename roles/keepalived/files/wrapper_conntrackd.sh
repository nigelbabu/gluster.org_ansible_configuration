#!/bin/bash
sed -i '/^Keepalived status:.*$/d' /etc/motd
echo "Keepalived status: $1" >> /etc/motd

if [ -f /usr/share/doc/conntrack-tools/doc/sync/primary-backup.sh ] ; then
    bash /usr/share/doc/conntrack-tools/doc/sync/primary-backup.sh $*
fi
