<?php

define('DB_USER', 'ajreinoso');
define('DB_PASS', '1234');
define('DB_HOST', 'localhost');

define('PATH_VENDOR', 'vendor/');
define('PATH_CALENDAR', PATH_VENDOR . 'calendar/');


// devuelve los registros de realizar la query a la BD 
function do_query($query)
{
	$conexion=mysql_connect(DB_HOST, DB_USER, DB_PASS)
	or die("Problemas en la conexion");

	mysql_select_db("test_analysis", $conexion) 
	or die("Problemas en la selección de la base de datos");

	$registros=mysql_query($query, $conexion) or
	die("Problemas en el select:".mysql_error());

	return $registros;
}


// http://emilio.aesinformatica.com/2009/05/07/comprobar-si-existe-una-tabla-con-php/
// Mira si la tabla existe en la BD
function table_exists($table_name) 
{ 
	$table = do_query("show tables like '" . $table_name . "'"); 

	if(mysql_fetch_row($table) === false)
		$exists = false;
	else
		$exists = true; 

	mysql_close($conexion);

	return $exists;
}

?>