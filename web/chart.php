<?php

require 'config.php';


class Chart
{
	//array multidimensional para dibujar las gráficas
	//e.g.:
	//[
	//	['Year', 'Sales', 'Expenses'],
	//	['2004',  1000,      400],
	//	['2005',  1170,      460],
	//	['2006',  660,       1120],
	//	['2007',  1030,      540]
	//]

	private $days;

	private $graphs;

	//para ver si se añarieron los días
	private function added_days()
	{
		return $this->data[0][0] == 'Day';
	}

	private function add_days()
	{
		echo 
	}
	/*
	Añade una gráfica a la tabla
	*/
	private function add_graph($graph)
	{
		switch ($graph["edition"]) {
			case 'ALL':
				$this->add
			break;
			
			default:
				# code...
			break;
		}
	}


	/*
	Devuelve la tabla a ser pintada

	@params
		$dates'i_date'] (fecha inicial)
			'f_date'] (fecha final)

		$graphs =
			array(
				"edition" => 'ES',
				"actions" => array(null, 0),
				"namespaces" => array(0, 4)
				,
				"edition" => 'ALL',
				"actions" => array(null, 0),
				"namespaces" => array(0, 4)
				,
				...
			)

		actions:
			null (visited) TABLA VISITED
			0 (edit) TABLA ACTIONS
			1 (history) 
			2 (save) TABLA SAVED
			3 (submit) NO INTERESA
			4 (search)

		namespaces:
			0 - article (main) el artículo en sí
			2 - ss  (talk) tablon de discusion para el artículo talk:squid
			3 - user 
			4 - user_talk
	*/
	function get_table($dates, $graphs)
	{
		// mysql> select day(day), count
		// -> from visited2009
		// -> where month(day)=5
		// -> and lang='EN'
		// -> and ns=0;

		// mysqlmysql> select month(day), count(*), sum(count) from visited2009 where lang='EN' and ns=0 group by month(day);

		// select month(day), count(*), sum(count) from visited2009 where lang='EN' and ns=0 and month(day) = 5 group by month(day);

		

		// tabla inicialmente con los días
		$table = array(
			array("Day")
			);


		foreach ($graphs as $graph) {
			add_graph($graph);
		}


		$query_all = "select day, count from visited2013 where ns=0 order by day";

		$regs = do_query($query);



		while ($reg=mysql_fetch_array($regs))
		{
	//[
	//	['Year', 'Sales', 'Expenses'],
	//	['2004',  1000,      400],
	//	['2005',  1170,      460],
	//	['2006',  660,       1120],
	//	['2007',  1030,      540]
	//]
			$arr[] = array($reg['day'], $reg['count']);
	// echo "Día: ".$reg['day']."<br>";
	// echo "Día de la semana: ".$reg['dayWeek']."<br>";
	// echo "Lenguaje: ".$reg['lang']."<br>";
	// echo "Namespace: ".$reg['ns']."<br>";
	// echo "Cantidad: ".$reg['count']."<br>";
		}

		mysql_close($conexion);

// echo var_dump($arr);

	private function print_table
		$sal = "[";
		$pos = 0;
		$current_day = 0;
		$ac_count = 0;
		foreach ($this->data as $row)
		{
			if($pos == 0){
				$sal .= "[";
				foreach ($row as $col) {
					$sal .= "'" . $col . "', '" . $value[1] . "'],";
				}
				$sal = substr_replace($sal ,"",-1);
				$sal .= "],";

				$pos++;
			}else{
				$day = $value[0];
				$count = $value[1];

				if($day != $current_day){
					if($current_day != 0){
						$sal .= "['" . $current_day . "', " . $ac_count . "],";
				// echo "['" . $current_day . "', " . $ac_count . "]," . "<br>";
					}
					$current_day = $day;
					$ac_count = $count;
				}else{
					$ac_count += $count;
				}
			}
		}
// quitamos la última coma y añadimos el corchete final
		$sal = substr_replace($sal ,"",-1);
		$sal .= "]";

		echo $sal;
	}


}



	


		?>