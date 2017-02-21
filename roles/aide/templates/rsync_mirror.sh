#!/bin/bash
/usr/bin/rsync -e ssh --delete-after -rqavz {{ user }}@{{ remote_server}}:{{ remote_dir }} {{ local_mirror }}
