<?php

require_once 'config.php';


// para sacar por pantalla el contenido de una variable
function see($var)
{
	echo "<br><br><br>" . var_dump($var) . "<br><br><br>";
}


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

//
function format($num)
{
	return (int)$num < 10 ? "0" . $num : $num;
}


//
// FECHAS
//


// devuelve las fechas primera y última registradas en la BD
function get_min_max_dates()
{
	// año inicial
	$i_year = 2000;
	// año final (el actual)
	$f_year = date('Y');

	// contiene, de todos los años, todos los días y meses detectados
	$dates = array(
		"min" => array(),
		"max" => array()
		);

	// sacamos la mínima
	for($year = $i_year; $year <= $f_year; $year++)
	{
		$table_name = "visited" . $year;
		if(table_exists($table_name))
		{
			$reg = do_query("select month(day), day(day) from " . $table_name .
				" order by day asc limit 1");
			if($d = mysql_fetch_row($reg))
			{
				$dates['min']['year'] = $year;
				$dates['min']['month'] = format($d[0]);
				$dates['min']['day'] = format($d[1]);

				mysql_close($conexion);
				break;
			}
		}
	}

	// sacamos la máxima
	for($year = $f_year; $year >= $i_year; $year--)
	{
		$table_name = "visited" . $year;

		if(table_exists($table_name))
		{
			$reg = do_query("select month(day), day(day) from " . $table_name .
				" order by day desc limit 1");
			if($d = mysql_fetch_row($reg))
			{
				$dates['max']['year'] = $year;
				$dates['max']['month'] = format($d[0]);
				$dates['max']['day'] = format($d[1]);

				mysql_close($conexion);
				break;
			}
		}
	}

	return $dates;
}


// corta una cadena YYYYMMDD en año, mes, día
function slice_date($date)
{
	$year = (int)(substr($date, 0, 4));
	$month = substr($date, 4, 2);
	$day = substr($date, 6, 2);

	return array(
		'year' => $year,
		'month' => $month,
		'day' => $day
		);
}


// pasa de YYYYMMDD a YYYY-MM-DD
function format_date($date)
{
	return substr($date, 0, 4) . '-' . substr($date, 4, 2) . '-' . substr($date, 6, 2);
}


// http://boonedocks.net/mike/archives/137-Creating-a-Date-Range-Array-with-PHP.html
function createDateRangeArray($strDateFrom,$strDateTo) {
	// takes two dates formatted as YYYY-MM-DD and creates an
	// inclusive array of the dates between the from and to dates.
	$aryRange=array();

	$iDateFrom=mktime(1,0,0, substr($strDateFrom,5,2), substr($strDateFrom,8,2),substr($strDateFrom,0,4));
	$iDateTo=mktime(1,0,0, substr($strDateTo,5,2), substr($strDateTo,8,2), substr($strDateTo,0,4));

	if($iDateTo>=$iDateFrom){
		array_push($aryRange,date('Y-m-d',$iDateFrom)); // first entry

		while($iDateFrom<$iDateTo){
			$iDateFrom+=86400; // add 24 hours
			array_push($aryRange,date('Y-m-d',$iDateFrom));
		}
	}

	return $aryRange;
}


?>