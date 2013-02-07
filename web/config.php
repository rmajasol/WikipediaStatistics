<?php

define('DB_USER', 'ajreinoso');
define('DB_PASS', '1234');
define('DB_HOST', 'localhost');

$conexion=mysql_connect(DB_HOST, DB_USER, DB_PASS)
	or die("Problemas en la conexion");

mysql_select_db("test_analysis", $conexion) 
  or die("Problemas en la selección de la base de datos");

$registros=mysql_query("select * from actions2013",$conexion) or
  die("Problemas en el select:".mysql_error());

while ($reg=mysql_fetch_array($registros))
{
  echo "Día: ".$reg['day']."<br>";
  echo "Día de la semana: ".$reg['dayWeek']."<br>";
  echo "Lenguaje: ".$reg['lang']."<br>";
  echo "Namespace: ".$reg['ns']."<br>";
  echo "Cantidad: ".$reg['count']."<br>";
}

mysql_close($conexion);
?>