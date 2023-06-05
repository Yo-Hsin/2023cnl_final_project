#!/bin/bash

username="${1}"
password="${2}"

#mysql_result=$(mysql \
#	--user="root" \
#	-e "SELECT * FROM radius.radcheck;")

#for row in ${mysql_result[@]}; do
#	printf $row
#	printf "\n"
#done

mysql -uroot radius<<EOFMYSQL
select count(*) from radcheck where username='$username' and value='$password';
EOFMYSQL
