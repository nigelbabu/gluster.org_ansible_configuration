#!/bin/bash

DIR=$1
pg_dumpall > $1/all.sql 
