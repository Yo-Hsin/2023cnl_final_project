#!/bin/bash

username="${1}"

mysql -uroot radius<<EOFMYSQL
select groupname from radusergroup where username='$username';
EOFMYSQL
