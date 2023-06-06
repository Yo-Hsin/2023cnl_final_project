#!/bin/bash

username="${1}"
password="${2}"
new_password="${3}"

mysql -uroot -h192.168.1.3 radius<<EOFMYSQL
update radcheck set value='$new_password' where username='$username' and value='$password';
EOFMYSQL
