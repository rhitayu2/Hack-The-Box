# Apache Hadoop 

- Running a Apache Hadoop Server.
- Login page and three current users:
	- tom
	- mark
	- rastating
- Login request sent in form of JSON object and as the name suggests maybe a Node JS application.
```bash
POST /api/session/authenticate HTTP/1.1
Host: 10.10.10.58:3000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json;charset=utf-8
Content-Length: 39
Origin: http://10.10.10.58:3000
Connection: close
Referer: http://10.10.10.58:3000/login

{"username":"admin","password":"admin"}
```

- [[Node/05 - Enumeration#Gobuster]]  Gives us an idea of the available js pages. Checking admin.js
```javascript
var controllers = angular.module('controllers');

controllers.controller('LoginCtrl', function ($scope, $http, $location) {
  $scope.authenticate = function () {
    $scope.hasError = false;

    $http.post('/api/session/authenticate', {
      username: $scope.username,
      password: $scope.password
    }).then(function (res) {
      if (res.data.success) {
        $location.path('/admin');
      }
      else {
        $scope.hasError = true;
        $scope.alertMessage = 'Incorrect credentials were specified';
      }
    }, function (resp) {
      $scope.hasError = true;
      $scope.alertMessage = 'An unexpected error occurred';
    });
  };
});
```

## Trying NoSQL injection

- Changing the login JSON format: 
```JSON
{
	"username" : "mark",
	"password" : {
		"$ne" : "1"
	}	
}
```

- We got bad request as response from Server. Specifically patched for nosql injection.
- From [[Node/05 - Enumeration#Manual Enumeration]] we can see there are multiple partials.
- The admin page might have a backup, but we need to be logged in as admin
![[Pasted image 20210331175529.png]]
- The source page isn't displaying anything other than the routes, we need to fuzz the /api of the webpage for other directories.
- 