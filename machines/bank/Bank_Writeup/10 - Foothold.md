# Foothold

![[Pasted image 20210408045412.png]]
- We can see most of the files are around size : 585,584,583,582,581
- If we can find an anomaly
```bash
curl http://bank.htb/balance-transfers > bank_transfers
cat balance_transfers | grep -v "584\|585\|582\|583\|581"    
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /balance-transfer</title>
 </head>
 <body>
<h1>Index of /balance-transfer</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="68576f20e9732f1b2edc4df5b8533230.acc">68576f20e9732f1b2edc4df5b8533230.acc</a></td><td align="right">2017-06-15 09:50  </td><td align="right">257 </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.7 (Ubuntu) Server at bank.htb Port 80</address>
</body></html>
```

- We can see `68576f20e9732f1b2edc4df5b8533230.acc` is around size 257.
`curl http://bank.htb/balance-transfers/68576f20e9732f1b2edc4df5b8533230.acc -o file.txt`
- file.txt has creds of chris.
- Login and go to support.php
- We can upload file, but only accepting image files. In source code, it is mentioned in \[DEBUG\] --> .htb files can be uploaded to be executed as php
- We can renmae our reverseshell to .htb, we can upload and get a reverse shell. Start listener on local machine before hand.
