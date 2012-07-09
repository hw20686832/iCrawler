#!/bin/bash
export PATH=/usr/kerberos/sbin:/usr/kerberos/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
export LD_LIBRARY_PATH=:/usr/local/apr/lib:/opt/instantclient_10_2:/usr/local/lib:/usr/lib
export NLS_LANG=American_America.UTF8
export ORACLE_HOME=/opt/instantclient_10_2

CATEGORY=$1

procnum=`pgrep -f "scrapy crawl ${CATEGORY}"`
if [ "${procnum}" = "" ]
then
    scrapy crawl $CATEGORY --nolog &
fi