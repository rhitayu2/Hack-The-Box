## Foothold
1. Running nmap we can get two ports 80 and 443.
2. 80 redirects to 443.
3. A login page. (15 invalid tries will block your IP)
4. Running gobuster with -x txt we get two useful files, system-user.txt and changelog.txt
5. system-users tell us the username is rohit and password as default company password, which from some googlin we can know is pfsense.
6. Login using those creds

## Priv Esc

7. Use searchsploit to get an exploit for remote code execution.
8. This hint can be taken from the changelof txt which states 2 of the 3 vulns have been fixed (https://www.proteansec.com/linux/pfsense-vulnerabilities-part-2-command-injection/).
9. Change the variables in the python script and run exploit.
10. What the script is this, the path : /status_rrd_graph_img.php?database=queues;[code]. We can use revshell or just enumerate using burp

