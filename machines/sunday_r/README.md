## Footlhold
(Ippsec)
1. Ran nmap and found 2 open ports : 79 and 111.
2. 79 runs a service called as finger service, which can give us information of the users, thus we can use this service to enumerate users. We can use the perl file and specify the word list from Seclist/usernames
3. We will get 3 users, sunny, sammy and root. 
4. Also we can run nmap on all ports and see ssh is hosted on 22022.
5. ssh sunny@10.10.10.76 -p 22022 -oKexAlgorithms=diffie-hellman-group1-sha1 is the command required to login.
6. We can use hydra and a password list to enumerate for sunny and sammy. We can get a match for sunny:sunday.
7. SSH to user sunny.

## Priv Esc
8. Run sudo -l to see that we can run /root/troll script.
9. Checking root folder there is a backups folder, which we can read (shadows file)
10. We can get the hash of both sunny and sammy.
11. hashcat -m 7400 to crack the passwords.
12. We get sammy:cooldude!
13. Ssh into sammy, we see we can run wget as sudo.
14. We can just get the root.txt using sudo wget -i(for in FILE searches) /root/root.txt
15. The box was lagging way too much so couldn't try this method.

===Method===
1. Login using both users sunny and sammy on different terminals.
2. We can use sammy to download a dummy script to /root/troll so it is overwritten. But if we can check we see that it is again written to just execute id as root.
3. So we have can host a file which would just execute bash. 
4. Download using wget to /root/troll and immediately execute using sunny, we can get a root shell.

