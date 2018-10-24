#!/bin/bash
/usr/bin/printf "%b" "Info: $NAGIOS_HOSTOUTPUT\n\n" | /bin/mail -s "$NAGIOS_HOSTNAME is $NAGIOS_HOSTSTATE ** $NAGIOS_LONGDATETIME" $NAGIOS_CONTACTEMAIL
