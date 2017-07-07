#!/bin/bash
if [ -f /usr/share/doc/conntrack-tools/doc/sync/primary-backup.sh ] ; then
    bash /usr/share/doc/conntrack-tools/doc/sync/primary-backup.sh $*
fi
