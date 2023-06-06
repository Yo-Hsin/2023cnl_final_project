#!/bin/bash

time_interval="${1}"

mysql -uroot -h192.168.1.3 radius<<EOFMYSQL
update radgroupcheck set value='$time_interval' where groupname='students' and attribute='Login-Time';
EOFMYSQL
