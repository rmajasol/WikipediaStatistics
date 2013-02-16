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


function slice_date($date)
{
	// corta una cadena YYYYMMDD en año, mes, día

	$year = substr($date, 0, 4);
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


function date_fmt($str_date)
{
	// devuelve si una fecha cumple el formato fmt dado

	switch (strlen($str_date)) {
		case 4:
		return 'YYYY';
		
		case 6:
		return 'YYYYMM';

		case 8:
		return 'YYYYMMDD';
	}
}


function dates_fmt($i_date, $f_date)
{
	// indica el formato de la petición, es decir, si queremos el resultado por
	// días, por meses o por años
	//
	// la prioridad es YYYYMMDD > YYYYMM > YYYY
	//
	// por ejemplo si i_date es YYYY y f_date YYYYMM, entonces devolverá
	// YYYYMM

	$i_date_fmt = date_fmt($i_date);
	$f_date_fmt = date_fmt($f_date);

	return strlen($i_date_fmt) > strlen($f_date_fmt) ? $i_date_fmt : $f_date_fmt;
}


function complete_dates($dates)
{
	// Si por ejemplo recibimos $dates['i_date'] como '2013' lo convertiremos en '20130101'
	// 
	// Como resultado obtenemos el mismo diccionario pero con las dos fechas 
	// completadas en YYYYMMDD

	$i_date = $dates['i_date'];
	$f_date = $dates['f_date'];
	$i_date_fmt = $dates['i_date_fmt'];
	$f_date_fmt = $dates['f_date_fmt'];
	$dates_fmt = $dates['dates_fmt'];

	switch ($dates_fmt) {
		case 'YYYY':
		// en este caso a las dos fechas hay que concatenarles '0101'
		$i_date .= "0101"; // YYYY0101
		$f_date .= "0101";
		break;

		case 'YYYYMM':
		if($i_date_fmt == 'YYYY')
		{
			$i_date .= "0101"; // YYYY0101
			$f_date .= "01"; 	// YYYYMM01
		}
		else if($f_date_fmt == 'YYYY')
		{
			$f_date .= "0101";
			$i_date .= "01";
		}
		else
		{
			$i_date .= "01";
			$f_date .= "01";
		}
		break;

		case 'YYYYMMDD':
		// aquí tenemos que comprobarlo contra YYYY e YYYYMM
		if($i_date_fmt == 'YYYY')
			$i_date .= "0101";
		else if($f_date_fmt == 'YYYY')
			$f_date .= "0101";

		if($i_date_fmt == 'YYYYMM')
			$i_date .= "01";
		else if($f_date_fmt == 'YYYYMM'){
			$f_date .= "01";
		}
		break;
	}

	return array(
		'i_date' 		=> $i_date,
		'i_date_fmt' 	=> $i_date_fmt,
		'f_date' 		=> $f_date,
		'f_date_fmt' 	=> $f_date_fmt,
		'dates_fmt'		=> $dates['dates_fmt']
		);
}


function get_f_date_sliced($dates)
{
	// Toma el diccionario $dates:
	//
	// $dates = array(
	// 'i_date' 		=> $i_date,
	// 'i_date_fmt' 	=> date_fmt($i_date),
	// 'f_date' 		=> $f_date,
	// 'f_date_fmt' 	=> date_fmt($f_date),
	// 'dates_fmt'		=> dates_fmt($i_date, $f_date)
	// );
	//
	// Devuelve la fecha final seteada en el formato:
	//
	// array(
	// 	'year' => $year,
	// 	'month' => $month,
	// 	'day' => $day
	// 	);

	$mktime = get_f_date_mktime($dates);
	$f_date_str = mktime_to_str($mktime);


	return slice_date($f_date_str); 
}


// se invoca dentro de set_f_date_dicc
function get_f_date_mktime($dates)
{
	// Nos servirá para setear la fecha final en función del formato.
	//
	// Devuelve un objeto tipo mktime
	//
	// Por ejemplo si las fechas son 2012 y 201302 entonces devolverá
	// 201302[ultimo_de_mes]
	//
	// S 
	//
	// $dates: diccionario con 
	//		$f_date['year'] 	'YYYY'
	//		$f_date['month']	'MM'
	//		$f_date['day']		'DD'
	// 
	// $dates_fmt: formato con el que pintaremos la gráfica
	//		'YYYY' seteamos $iDateTo a el año siguiente menos un día
	//		'YYYYMM' el mes siguiente menos un día
	//
	//		En el caso de 'YYYYMMDD' no es necesario hacer nada,
	//		devolviendo la fecha tal cual

	// see($dates);

	$f_date = slice_date($dates['f_date']);
	$month = (int)$f_date['month'];
	$day = (int)$f_date['day'];
	$year = (int)$f_date['year'];

	$f_date_fmt = $dates['f_date_fmt'];
	$dates_fmt = $dates['dates_fmt'];

	switch ($dates_fmt) {
		// 2012
		case 'YYYY':
		$day--;
		$year++;
		break;

		case 'YYYYMM':
		if($f_date_fmt == 'YYYY')
		{
			$day --;
		}
		else
		{
			$month++;
			$day--;
		}

		case 'YYYYMMDD':
		if($f_date_fmt == 'YYYYMM')
		{
			$day--;
		}
	}

	return mktime(1,0,0, $month, $day, $year);
}


// se invoca dentro de set_f_date_dicc
function mktime_to_str($mktime)
{
	// recibe un objeto mktime y devuelve un string en formato YYYYMMDD
	
	$d = date('Y-m-d',$mktime);

	$year = substr($d, 0, 4);
	$month = substr($d, 5, 2);
	$day = substr($d, 8, 2);

	return $year . $month . $day;
}


function set_f_date_dicc()
{
	// Devuelve un diccionario para la fecha a partir de setear la fecha final en
	// función del formato usado
	//
	// $f_date: diccionario con 
	//		$f_date['year'] 	'YYYY'
	//		$f_date['month']	'MM'
	//		$f_date['day']		'DD'

	$mktime = set_f_date_mktime($f_date, $dates_fmt);

	return mktime_to_str($mktime);
}


function date_to_time($date)
{
	// http://www.highlystructured.com/comparing_dates_php.html
	//
	// Transforma un diccionario (year, month, day) en un objeto time
	$date = slice_date($date);
	$d = $date['year'] . "-" . $date['month'] . "-" . $date['day'];

	return strtotime($d);
}


function gen_dates_arr($dates) {
	// modificado de:
	// http://boonedocks.net/mike/archives/137-Creating-a-Date-Range-Array-with-PHP.html
	// takes two dates formatted as YYYYMMDD and creates an
	// inclusive array of the dates between the from and to dates.
	//
	// Esto nos servirá para pintar el eje de las fechas
	//
	// Por ejemplo si el formato es YYYYMM y las fechas inicial y final 2012, 201202,
	// entonces pintará desde 201201 hasta 201202 inclusive

	// see($d);
	
	// $iDateFrom = mktime(1,0,0, $i_date['month'], $i_date['day'], $i_date['year']);
	// $iDateTo = mktime(1,0,0, $strDateTo['month'], $strDateTo['day'], $strDateTo['year']);
	// cambiamos la fecha final dependiendo del formato a usar
	$iDateFrom = date_to_time($dates['i_date']);
	$iDateTo = get_f_date_mktime($dates);  

	$date = date('Y-m-d', $iDateFrom);
	$dates_arr = array();

	switch ($dates['dates_fmt']) {

		case 'YYYY':
		for($i=0; $iDateFrom < $iDateTo; $i++){
			$add_not_zero = $i == 1 ? "+1 year" : "+" . $i . " years";
			$add = $i == 0 ? "" : $add_not_zero;
			// http://stackoverflow.com/questions/3642652/get-current-date-and-date-after-two-months-in-php
			$iDateFrom = strtotime($date . $add);
			array_push($dates_arr,date('Y',$iDateFrom));
		}		
		break;

		case 'YYYYMM':
		for($i=0; $iDateFrom < $iDateTo; $i++){
			$add_not_zero = $i == 1 ? "+1 month" : "+" . $i . " months";
			$add = $i == 0 ? "" : $add_not_zero;
			$iDateFrom = strtotime($date . $add);
			array_push($dates_arr,date('Y-m',$iDateFrom));
		}
		break;

		case 'YYYYMMDD':
		for($i=0; $iDateFrom < $iDateTo; $i++){
			$add_not_zero = $i == 1 ? "+1 day" : "+" . $i . " days";
			$add = $i == 0 ? "" : $add_not_zero;
			$iDateFrom = strtotime($date . $add);
			array_push($dates_arr,date('Y-m-d',$iDateFrom));
			// see($dates_arr);
		}
		break;
	}

	// see($dates_arr);

	// quitamos el elemento de más que siempre aparece..
	array_pop($dates_arr);

	return $dates_arr;
}


?>