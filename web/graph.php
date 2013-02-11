<?php

require 'functions.php';
require 'config.php';

$edition = $_POST['edition'];
$action = $_POST['action'];

echo "Res: " . $edition . ", " . $action;


// devuelve todas las fechas entre una inicial y final dadas
function get_dates($i_date, $f_date)
{
	$i_date = slice_date($i_date);
	$f_date = slice_date($f_date);

	// año inicial y final
	$i_year = $i_date['year'];
	$f_year = $f_date['year'];

	// contendrá todas las fechas devueltas por la consulta
	$dates = array();

	$curr_year = $i_year;
	// sacamos la mínima
	for(; $curr_year <= $f_year; $curr_year++)
	{
		$table_name = "visited" . $curr_year;
		if(table_exists($table_name))
		{

			$query = "select day from " . $table_name;

			if($f_year > $curr_year)
			{
				if($curr_year == $i_year)
				{
					$query .= " where day > " . 
					"'" . $curr_year . "-" . $i_date['month'] . "-" . $i_date['day'] . "'";
				}
			}
			else
			{
				if($curr_year == $i_year)
				{
					$query .= " where day > " . 
					"'" . $curr_year . "-" . $i_date['month'] . "-" . $i_date['day'] . "'" .
					" and day < " .
					"'" . $curr_year . "-" . $f_date['month'] . "-" . $f_date['day'] . "'";
				}
				else
				{
					$query .= " where day < " .
					"'" . $curr_year . "-" . $f_date['month'] . "-" . $f_date['day'] . "'";
				}
			}
		}

		$query .= " order by day asc";

		$reg = do_query($query);
		while($day = mysql_fetch_array($reg))
			$dates[] = $day['day'];
	}

	mysql_close($conexion);
}

// function get_graph($edition, $action)
// {

// 	$query = "select day, count from ";

// 	switch ($action) {
// 		case 'null':
// 			visited2013 where ns=0 order by day"
// 			break;

// 		default:
// 			# code...
// 			break;
// 	}
// 	if($action == 'ALL')
// 	{

// 	}
// }
?>