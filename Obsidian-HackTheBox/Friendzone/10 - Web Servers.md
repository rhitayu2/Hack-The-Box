# Web Servers

## Port 80

- Visiting the website we get one more domain : frienzoneportal.red
![[Pasted image 20210329101601.png]]

## Checking credentials from [[Friendzone/00 - Loot]]
- Checking in https://admin.friendzoneportal.red/login.php
![[Pasted image 20210329105008.png]]

- Checking on administrator1.friendzone.red
![[Pasted image 20210329105038.png]]

- Visiting dashboard.php
![[Pasted image 20210329105218.png]]
- Thus we need to pass the image params, this might help when we upload an image on uploads.domain and then we can use this domain to execute it.
- After seeing /images in administrator1.friendzone.red/ we can see that there are two images, but files are not uploading in uploads.friendzone.red
![[Pasted image 20210329110736.png]]
![[Pasted image 20210329110746.png]]
- Till now we don't see the use of timestamp param.
- So was wrong, had to see the ippsec video once, timestamp is calling the file, so there is potential LFI
- Using php://filter/convert.base64-encode/resource={file to be read}. It will return a base64 string of the file encoded.