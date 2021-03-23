## Foothold

1. Running nmap on 10.10.10.218, we get three ports are open 22,80,9001
2. Visiting 80 and 9001, requires authorisation. 9001 is running medusa server framework, which is a supervisor.
3. Tried running exploit/linux/http/supervisor_xmlrpc_exec from msf console, didn't work.
4. We can see in 80 port, there is a robots.txt, /weather present on it. 
5. Running gobuster with wordlist gives us idea of /weather/forecast present. The city=list parameters gives us all the cities. Need to pass it in the GET or POST parameter.
6. Checked with city_list.py regarding the outputs. Can use code injection to get a reverse shell from the parameters. Payload present in file. The box is named Luanne, hint towards lua language being used. Also on nmap we found NetBSD server is running, therefore payload created with these hints.
7. Putting a POST request and a listener running, we can get back a shell. We see the user is webapi_user. 

## Priv Esc

8. We can see a hash of the password in .htppasswd and find the hash is md5 crypt. We can crack it using hashcat(mode 500) or john. Password is iamthebest
9. Now we can login, but no use. There was a localhost server running on the box.
10. curl --user webapi_user:iamthebest 127.0.0.1/~r.michaels/id_rsa. We can see that there is a user r.michaels and the ssh port is running. We can use the curl command to get the ssh_keys from the user's directory. We can use it to login --> ssh -i <filename> r.michaels@10.10.10.218
11. We can see there is the user.txt. We can also see there is a backup directory. There is an encoded file, we can use openssl or netpgp to decrypt it and store it somewhere where we can use tar xvf to unpack it.
12. Upon unpacking there is a .htpppasswd file again. Crack it using john.
13. We get the password: littlebear.
14. Login as root. doas su. Cat the root.txt

