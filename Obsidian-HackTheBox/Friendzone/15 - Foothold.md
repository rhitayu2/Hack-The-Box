# Foothold

## Getting reverse shell
- Using the payload, file included can be the upload script, as we are saving our reverse shell in some directory, visiting that we can execute or revshell.
- file_name : /../uploads/upload
```php
<?php

// not finished yet -- friendzone admin !

if(isset($_POST["image"])){

echo "Uploaded successfully !<br>";
echo time()+3600;
}else{

echo "WHAT ARE YOU TRYING TO DO HOOOOOOMAN !";

}

?>

```
- From the screenshot, we can see it isn't uploading to any directory. There is another possibility, we were able to put it in Development share of the samba server
- We need to enumerate to that directory and execute our reverse shell. Files was in /etc/Files, so taking a guess that Development is in /etc/Development.
- To check we are uploading a test php file called new.php, which would just print hello
```php
<?php
	echo "Hello" ;
?>
```
- url: https://administrator1.friendzone.red/dashboard.php?image_id=a.jpg&pagename=../../../etc/Development/new
![[Pasted image 20210329174908.png]]
- So we get RCE. We can upload our revshell script. (In the directory).
-  visiting https://administrator1.friendzone.red/dashboard.php?image_id=a.jpg&pagename=../../../etc/Development/revshell
![[Pasted image 20210329175221.png]]