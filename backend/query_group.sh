#!/bin/bash

username="${1}"

mysql -uroot -h192.168.1.3 radius<<EOFMYSQL
select groupname from radusergroup where username='$username';
EOFMYSQL
