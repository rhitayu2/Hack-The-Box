<?php

require 'vendor/autoload.php';                                                     
use Aws\DynamoDb\DynamoDbClient;                                                   
if($_SERVER["REQUEST_METHOD"]==="POST") {                                          
        if($_POST["action"]==="get_alerts") {                                      
                date_default_timezone_set('America/New_York');                     
                $client = new DynamoDbClient([                                     
                        'profile' => 'default',                                    
                        'region'  => 'us-east-1',                                  
                        'version' => 'latest',                                     
                        'endpoint' => 'http://localhost:4566'                      
                ]);                                                                
                                                                                   
                $iterator = $client->getIterator('Scan', array(                    
                        'TableName' => 'alerts',                                   
                        'FilterExpression' => "title = :title",
                        'ExpressionAttributeValues' => array(":title"=>array("S"=>"Ransomware")),
                ));                      

                foreach ($iterator as $item) {
                        $name=rand(1,10000).'.html';
                        file_put_contents('files/'.$name,$item["data"]);
                }                        
                passthru("java -Xmx512m -Djava.awt.headless=true -cp pd4ml_demo.jar Pd4Cmd file:///var/www/bucket-app/files/$name 800 A4 -out files/result.pdf");
        }                                
}                                        
else                                     
{                                        
?>                                       

