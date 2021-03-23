## Foothold

1. Run nmap and a bunch of ports are open, we can check the port 80 connection.
2. We see an elastix login page.
3. Use searchsploit to get the local file inclusion file, which we can just take the payload from.
4. Visiting the site we can see bunch of passwords.
5. A shortcut to getting the user flag would be just include /home/fanis/user.txt after enumerating the other users.
6. We can get the user list with valid login in /etc/passwd.
7. We can just try all the passwords with the users. We will get a valid hit for root.
8. Cat out the root.txt
