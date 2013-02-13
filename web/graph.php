<?php

require 'functions.php';

// echo json_encode('hola!!');
// echo var_dump(json_decode($_POST['chart']));

// $edition = $_POST['edition'];
// $action = $_POST['action'];

// echo "Res: " . $edition . ", " . $action;

// array con todas las fechas en el intervalo

// decodificamos lo que recibimos en la petición AJAX
$chart = json_decode($_POST['chart']);


//
// FECHAS INICIAL Y FINAL
//
// $i_date = format_date($chart->{'i_date'});
// $f_date = format_date($chart->{'f_date'});
// $i_date = '20130101';
// $f_date = '20130110';
$i_date = $chart->{'i_date'};
$f_date = $chart->{'f_date'};

$dates = createDateRangeArray(format_date($i_date), format_date($f_date));


// array(426) { [0]=> string(10) "2012-01-01" [1]=> string(10) "20

//
// GRÁFICAS
//
$received_graphs = $chart->{'graphs'};
// echo $graphs[0]->{'edition'};

// populamos un array 'graphs' a partir de los gráficos recibidos en JSON
$graphs = array();
foreach ($received_graphs as $graph) {
	$graphs[] = array(
		"edition" => $graph->{'edition'},
		"action" => $graph->{'action'}
		);
}

// $graphs = array(
// 	array(
// 		"edition" => 'ALL',
// 		"action" => 'null'
// 		),
// 	array(
// 		"edition" => 'ALL',
// 		"action" => '2'
// 		),
// 	);

// see(get_json($dates, $graphs));
// echo get_json($dates, $graphs);
echo get_json($dates, $graphs);





function get_json($dates, $graphs)
{
	// inicializamos el resultado a devolver en la respuesta AJAX,
	// añadiendo en la primera fila el array de fechas..
	$raw_result = array(
		"dates" => $dates,
		"graphs" => array()
		);

	foreach ($graphs as $graph) {

		// añadimos la fila generada al resultado
		$graph_key = $graph['edition'] . "_" . get_action_name($graph['action']);
		$raw_result['graphs'][$graph_key] = gen_row($graph);
	}

	// $json = json_encode($result);
	// see($json);

	// see($raw_result);

	$result = transform($raw_result);
	
	// see($result);

	return json_encode($result);
}


function transform($raw_result)
{
	//
	// CONTENIDO DE $raw_result:
	//
	// "{
	// "dates":["2013-01-01","2013-01-02","2013-01-03","2013-01-04","2013-01-05","2013-01-06",
	// "2013-01-07","2013-01-08","2013-01-09","2013-01-10"],
	//
	// "graphs":{
	//		"ALL_visited":[
	//			["2013-01-01","7433"],["2013-01-02","7474"],["2013-01-03","7625"],
	//			["2013-01-04","7315"],["2013-01-05","7482"]],
	//		"ALL_saved":[
	//			["2013-01-02","5"],["2013-01-03","4"],["2013-01-04","1"],
	//			["2013-01-05","5"]]
	//		}
	// }" 

	//
	// CONTENIDO DE $result tras hacer 'transform($raw_result)':
	//
	// "{
	// "dates":["2013-01-01","2013-01-02","2013-01-03","2013-01-04","2013-01-05","2013-01-06",
	// "2013-01-07","2013-01-08","2013-01-09","2013-01-10"],
	//
	// "graphs":{
	//		"ALL_visited":["7433","7474","7625","7315","7482"],
	//		"ALL_saved":["0","5","4","1","5"]
	//		}
	// }" 

	$dates = $raw_result['dates'];
	$raw_graphs = $raw_result['graphs'];
	
	// see($raw_result);

	$result = array(
		'dates' => $dates,
		'graphs' => array()
		);

	// recorremos las gráficas 'en crudo' del objeto raw_result
	foreach ($raw_graphs as $raw_graph_key => $raw_graph_data) 
	{
		
		//["0","7","5","0",...]
		$graph_result_data = array();

		// recorremos las fechas para cada gráfica de result
		foreach ($dates as $date) 
		{

			// recorremos cada par ["2012-01-28","7361"] como $data
			// $data[0] es "2012-01-28", y data[1] "7361"
			$found_data = False;
			foreach ($raw_graph_data as $data) 
			{
				if($date === $data[0])
				{
					$graph_result_data[] = $data[1];
					$found_data = True;
					break;
				}
			}
			if(!$found_data)
			{
				$graph_result_data[] = "0";
			}
		}

		$result['graphs'][$raw_graph_key] = $graph_result_data;
	}

	// see($result);
	return $result;
}


function get_table_name($action)
{
	// devuelve el nombre de la tabla a consultar dada una acción
	// 		actions:
	// 			null (visited) TABLA VISITED
	// 			0 (edit) TABLA ACTIONS
	// 			1 (history) 
	// 			2 (save) TABLA SAVED
	// 3 (submit) NO INTERESA
	// 			4 (search)

	// 		namespaces:
	// 			0 - article (main) el artículo en sí
	// 			2 - ss  (talk) tablon de discusion para el artículo talk:squid
	// 			3 - user 
	// 			4 - user_talk
	switch ($action) {
		case 'null':
		return 'visited';
		case '2':
		return 'saved';
		default:
		return 'actions';
	}
}


// devuelve el nombre de la acción a partir de su código
function get_action_name($action)
{
	switch ($action) {
		case 'null':
		return 'visited';
		
		case '1':
		return 'history';

		case '2':
		return 'saved';

		case '4':
		return 'search';
	}
}


function gen_row($graph)
{
	// genera un array con el resultado de hacer la petición a la BD
	//
	// 	[
	//		["2012-01-28","7361"],["2012-01-29","7349"],["2012-01-30","7366"],
	//		["2012-01-31","7182"],["2012-02-01","7211"],["2012-02-02","7163"],
	//		["2012-02-03","7114"]
	//	]

	$i_date = slice_date($GLOBALS['i_date']);
	$f_date = slice_date($GLOBALS['f_date']);

	// año inicial y final
	$i_year = $i_date['year'];
	$f_year = $f_date['year'];

	// contendrá todas las fechas y counts devueltas por la consulta.
	// Se irá llenando en cada iteración. Si por ejemplo queremos
	// consultar sobre 3 años habrán 3 iteraciones, por lo que tendremos que ir
	// acumulando los resultados en algún sitio
	$arr = array();
	
	for($year = $i_year ; $year <= $f_year; $year++)
	{
		$table_name = get_table_name($graph['action']) . $year;
		if(table_exists($table_name))
		{

			$query = "select day, sum(count) from " . $table_name . " where ns=0";

			if($graph['edition'] != 'ALL')
				$query .= " and lang='" . $graph['edition'] . "'";

			// si la tabla es actionsYYYY entonces elegimos la acción
			if(get_table_name($graph['action']) == 'actions')
				$query .= " and action=" . $graph['action'];


			//
			// selección de fechas según el año por el que vayamos iterando
			//
			// 2013 > 2012
			if($f_year > $year && $year == $i_year)
			{
				$query .= " and day >= " . 
				"'" . $year . "-" . $i_date['month'] . "-" . $i_date['day'] . "'";
			}
			// 2013 == 2013
			else
			{
				// 2013 == 2012
				if($year == $i_year)
				{
					$query .= " and day >= " . 
					"'" . $year . "-" . $i_date['month'] . "-" . $i_date['day'] . "'" .
					" and day <= " .
					"'" . $year . "-" . $f_date['month'] . "-" . $f_date['day'] . "'";
				}
				// 2013 != 2012
				else
				{
					$query .= " and day <= " .
					"'" . $year . "-" . $f_date['month'] . "-" . $f_date['day'] . "'";
				}
			}

			$query .= " group by day order by day asc";

			$regs = do_query($query);
			while($row = mysql_fetch_array($regs))
				$arr[] = array($row['day'], $row['sum(count)']);
		}
	}

	mysql_close($conexion);

	// see($arr);
	
	return $arr;

}



?>