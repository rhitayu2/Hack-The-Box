## Foothold

1. Nmap scan, gave us open ports 22,80.
2. Visit Site, CMS for news. Top news i s fail2ban. Cannot bruteforce directory, thus cannot use gobuster. 
3. Inspect element, we can see there are many js files in the CuteNews directory, try that.
4. Login page. We can create a user, lowest privilege, and we can upload avatar.

### Two methods of exploitation

	===Method 1===
	1. The site is PHP based, can be checked from documentation. Thus a PHP rev shell, prepend with GIF8;
	2. Documentation gives us that the uploads are done in /CuteNews/uploads.
	3. Open listener, execute revshell.php

	===Method 2===
	1. Find exploit regarding cute news avatar upload vulnerability. (https://www.exploit-db.com/exploits/46698)
	2. Put it in msf/exploits/modules. Then reload_all.
	3. Set parameters, run and drop shell.

## Priv Escalation

5. Now that we have a shell we can enumerate. We can find in /CuteNews/cdata/lines that it is a big chunk of base64 encoding. Decode it, we get SHA2-256 hash for user paul. 
6. We have enumerated to know that there are two users, paul and nadav.
7. hashcat -m 1400 paul_hash rockyou. paul:atlanta1
8. Enumerate again, using linpeas, we get authorized_keys have nadav's pub key as same as paul's. 
9. Copy paul's ssh key and chmod, then ssh -i -id_rsa_paul nadav@10.10.10.206
10. Hardest Part. Enumerate all again.
11. (https://unit42.paloaltonetworks.com/usbcreator-d-bus-privilege-escalation-in-ubuntu-desktop/)
12. The vulnerability can be seen in .viminfo, where d-bus was mentioned.
13. gdbus call --system --dest com.ubuntu.USBCreator --object-path /com/ubuntu/USBCreator --method com.ubuntu.USBCreator.Image /root/.ssh/id_rsa /tmp/temp_id.txt.
14. This can be used many ways, directly copy the root.txt to the file in tmp, or copy root's ssh file and login, using that.
