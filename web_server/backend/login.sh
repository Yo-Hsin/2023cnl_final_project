#!/bin/bash

username="${1}"
password="${2}"

mysql -uroot -h192.168.1.3 radius<<EOFMYSQL
select count(*) from radcheck where username='$username' and value='$password';
EOFMYSQL
