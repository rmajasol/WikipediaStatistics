<?php


require 'config.php';

// <div id="i_selects">
// 	<select id="i_year">
// 		<option value="20">2012</option>
// 		<option value="2013">2013</option>
// 	</select>
// 	<select id="i_month">
// 		<option value="2012">2012</option>
// 		<option value="2013">2013</option>
// 	</select>
// 	<select id="i_day">
// 		<option value="2012">2012</option>
// 		<option value="2013">2013</option>
// 	</select>
// </div>

// <div id="f_selects">
// 	<select id="f_year">
// 		<option value="2012">2012</option>
// 		<option value="2013">2013</option>
// 	</select>
// 	<select id="i_year">
// 		<option value="2012">2012</option>
// 		<option value="2013">2013</option>
// 	</select>
// 	<select id="i_year">
// 		<option value="2012">2012</option>
// 		<option value="2013">2013</option>
// 	</select>
// </div>

// genera una serie de opciones para un <selector> dado un valor inicial y final
function gen_options($i_value, $f_value)
{
	for(; $i_value <= $f_value; $i_value++)
		echo "<option value='" . $i_value . "'>" . $i_value . "</option>";
}


// devuelve un conjunto de meses y días detectados en la BD para un año dado
function get_dates($year)
{
	$dates = array(
		"year" => $year,
		"months" => array(),
		"days" => array()
	);

	// Si la tabla existe para ese año inyectamos todos los meses y días que hay
	$table_name = "visited" . $year;

	if(table_exists($table_name))
	{
		$regs = do_query("select month(day), day(day) from " . $table_name .
			" group by day order by day asc");

		while ($reg=mysql_fetch_array($regs))
		{
			$dates['months'][] = $reg['month(day)'];
			$dates['days'][] = $reg['day(day)'];
		}
	}

	return $dates;
}


// devuelve todas las fechas existentes en la BD
function get_all_dates()
{
	// año inicial
	$year = 2000;
	// año final (el actual)
	$f_year = date('Y');

	$years = array();
	for(; $year <= $f_year; $year++)
		$years[] = get_dates($year);

	return $years;
}


// consulta en la BD cada fecha existente para generar un grupo de selectores
// con dichas fechas
function gen_date_selector($type)
{	
	
		


	// echo <select name="i_year">
	// 		<option value="20">2012</option>
	// 		<option value="2013">2013</option>
	// 	</select>	
}
?>