#!/bin/bash

time_interval="${1}"

mysql -uroot radius<<EOFMYSQL
update radgroupcheck set value='$time_interval' where groupname='students' and attribute='Login-Time';
EOFMYSQL
