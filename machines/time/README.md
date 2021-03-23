## Foothold

1. Running nmap, we see there are two ports open. 22 and 80.
2. Visiting the website we can see that it is a website to make json objects look better. There is a mode (mode = 2 from burpsuite) to validate. We can see that the error from java library Jackson has not been sanitised.
3. We can find a vulnerability in this github repo https://github.com/jas502n/CVE-2019-12384
4. Host the payload file on local server and validate the rb file from the github repo.
5. netcat from the victim's side is not working properly so using another rev shell.

## Priv Esc

6. Upon logging in we can see that we are a user called as pericles and we can access the user.txt
7. Upon running linpeas we can see that there is a file in /usr/bin called as timer_backup.sh. And from linpeas we can see that root has been executing the shell script.
8. We can use this to escalate privilge. Two methods:

Method 1
========
a. Append to the shell script "cat /root/root.txt > /tmp/new". Tried to append the private key, but ssh private key not present.

Method 2
=======
a. create new private and public keys and we had seen that root was Hashing known hosts. Echo out the public key in /root/.ssh/authorized_keys
b. login as root using -i id_rsa (private key)

