# Initial Foothold

1. Add delivery.htb and helpdesk.delivery.htb to the /etc/hosts.
2. We can run nmap, but the sites are listed under their website, Mainly helpdesk and mattermost hosted on another port, which can be accessed through their Contact Us page.
3. We can create a new ticket and then we get the ticket number and can view the ticket. All the updates regarding the tickets should be available under this page. We should also note that there should be an email with the ticket number. 
4. This email is listed so that all the issues regarding the ticket can be sent on this email and the thread will be updated. We can exploit this fact and send the verification email for the ticket number, additionally this would be registered with @delivery.htb, thus we can login using this.
5. Now we can login to the matter most server and see that there is an existing team "internal"
6. Initial user creds are already provided. cat out the user.txt

## Priv Esc
7. After logging in with the user we can check out /opt/mattermost/config and see that there is a config.json file present on the system. It has the creds for the mmuser which can log into the mysql server. We can see the the user table.
8. select Password from Users where Username like "root"; 
9. We can see its a bcrypt password, or we can even check it.
10. We had also seen the password text was "PleaseSubscribe!" from the internal teams log from the mattermost dashboard.
11. hashcat -a 0 -m 3200 passwordHash.file PleaseSubscribe.file -r /usr/share/hashcat/rules/best64.rule 
12. Give it time to get the hashed password. --> PleaseSubscribe!21
 
