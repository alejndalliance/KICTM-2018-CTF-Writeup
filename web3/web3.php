<?php
$servername = "localhost";
$username = "xxx";
$password = "xxx";
$dbname = "xxx";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//data: atoh(l+','+p)+'+'+md5(atoh(l+','+p)); 
$data=explode(" ", $_GET['data']);
if (md5($data[0]) != $data[1])
{
	die("Invalid input data !");
}
$data1=explode(",", hex2bin($data[0]));
$user=base64_decode($data1[0]);
$pass=base64_decode($data1[1]);
//die($user." ".$pass);

file_put_contents('k8_log.txt', $_SERVER['REMOTE_ADDR']." : ".$user."  |  ".$pass."\n", FILE_APPEND);

$sql = "SELECT auth FROM web3 where login='$user' AND pass=PASSWORD('$pass')" ;
$result = $conn->query($sql);

if (!$result) die("Query error !"); 

if ($row = $result->fetch_assoc()) {
	if ($row['auth'] == '1')
	{
		echo "The flag is PffftHHhhhW3bHack1ngiz34zyL0L@kictm2018 :) ";
	}
	else
	{
		echo "You are not authorized to view this resource !";
	}
}
else
{
	echo "Invalid Username/Password !";
}
$conn->close();