## Foothold

1. Run nmap and we can see that there are two ports open: 80 and 22
2. Open web page and view-source, we can see that there is a directory called as nibbleblog.
3. A CMS wesite therefore, run gobuster, we get admin.php and /content. /content tells us there is a user called as admin
4. We can try common passwords in admin.php. admin:nibbles work.
5. We can check a RCE (https://curesec.com/blog/article/blog/NibbleBlog-403-Code-Execution-47.html). Upload rev shell, open listener and execute from /content/private/plugins/my_image/php.
6. We get a revshell for nibbler and can cat out the user.txt

## Priv Esc

7. Run sudo -l, which takes a while to run, which shows we can run the script /home/nibbler/personal/stuff/monitor.sh as root.
8. Thus we can do two things, either append "cat root.txt" or append a bash rev shell.
9. Execute sudo /home/nibbler/personal/stuff/monitor.sh

## Extra

10. So instead of unzipping personal.zip we can directly make a directory and execute bash in the script. Don't forget to add the shebang.
11. The delay in sudo -l was because Nibbles as a host cannot eb resolved as it is hosted on the Shocker VM. We can just add 127.0.0.2 Nibbles to /etc/host.
12. We can also use Rational Love kernel exploit. We need to compile on the victim machine to make it work
13. Also added a python script to directly get revshell, on port 9002, change ip and port accordingly.
