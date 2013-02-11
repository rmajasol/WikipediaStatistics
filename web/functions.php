<?php

require_once 'config.php';


//
function format($num)
{
	return (int)$num < 10 ? "0" . $num : $num;
}


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
	for(; $i_year <= $f_year; $i_year++)
	{
		$table_name = "visited" . $i_year;
		if(table_exists($table_name))
		{
			$reg = do_query("select month(day), day(day) from " . $table_name .
				" order by day asc limit 1");
			if($d = mysql_fetch_row($reg))
			{
				$dates['min']['year'] = $i_year;
				$dates['min']['month'] = format($d[0]);
				$dates['min']['day'] = format($d[1]);

				mysql_close($conexion);
				break;
			}
		}
	}

	// sacamos la máxima
	for(; $f_year >= $i_year; $f_year--)
	{
		$table_name = "visited" . $f_year;

		if(table_exists($table_name))
		{
			$reg = do_query("select month(day), day(day) from " . $table_name .
				" order by day desc limit 1");
			if($d = mysql_fetch_row($reg))
			{
				$dates['max']['year'] = $i_year;
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
	$month = (int)(substr($date, 4, 6));
	$day = (int)(substr($date, 6, 8));

	return array(
		'year' => $year,
		'month' => $month,
		'day' => $day
		);
}


?>