google.load("visualization", "1", {packages:["corechart"]});

var min_date;
var max_date;

// esta variable contendrá cada gráfica devuelta vía AJAX
var graphs = [];
// fechas inicial y final

var i_date;
var i_year;
var i_month;

var f_date;
var f_year;
var f_month;


$(document).on('ready', function(){

	min_date = $("#date_selectors input[name=i_date]").val();
	max_date = $("#date_selectors input[name=f_date]").val();

	var date_selectors = $("#date_selectors input[type=text]");
	date_selectors.on('keyup', refreshChart);

	var add_graph_link = $("#graph_selectors a");
	add_graph_link.on('click', displayGraphSelector);
});


function setErrorBox(msg)
{
	$("#error_box").show();
	$("#error_box").text(msg);
}



function sliceDate_toInt(field)
{
	// divide cadena YYYYMMDD en diccionario con año, mes, día enteros
	
	var year = parseInt(field.substring(0, 4), 10);
	var month = parseInt(field.substring(4, 6), 10);
	var day = parseInt(field.substring(6, 9), 10);

	return {
		year: year,
		month: month,
		day: day
	};
}


function sliceDate_toStr(field)
{
	// divide cadena YYYYMMDD en diccionario de strings con año YYYY, mes MM, día DD

	var year = field.substring(0, 4);
	var month = field.substring(4, 6);
	var day = field.substring(6, 9);

	return {
		year: year,
		month: month,
		day: day
	};
}


function date_fmt(field)
{
	// indica el formato de la fecha: YYYY, YYYYMM, YYYYMMDD o formato no válido

	// http://www.9lessons.info/2009/03/perfect-javascript-form-validation.html
	var regexp_yyyy = /^[0-9]{4}$/;
	var regexp_yyyymm = /^[0-9]{6}$/;
	var regexp_yyyymmdd = /^[0-9]{8}$/;

	field = field.toString();

	if(regexp_yyyy.test(field))
		return 'YYYY';
	if(regexp_yyyymm.test(field))
		return 'YYYYMM';
	if(regexp_yyyymmdd.test(field))
		return 'YYYYMMDD';

	if(field === 'init')
	{
		i_date = min_date;
		return 'YYYYMMDD';
	}

	if(field === 'end')
	{
		f_date = max_date;
		return 'YYYYMMDD';
	}

	return 'invalid';
}


function formatOk(field)
{
	// comprobamos si está bien escrito el campo

	if(date_fmt(field) === 'invalid')
	{
		setErrorBox("Introduzca fechas en formatos: YYYY, YYYYMM o YYYYMMDD, " +
			"o bien introduzca 'init' y/o 'end'");
		return false;
	}

	return true;
}


function dates_fmt(i_date, f_date)
{
	// indica el formato de la petición, es decir, si queremos el resultado por
	// días, por meses o por años
	//
	// la prioridad es YYYYMMDD > YYYYMM > YYYY
	//
	// por ejemplo si i_date es YYYY y f_date YYYYMM, entonces devolverá
	// YYYYMM

	i_date_fmt = date_fmt(i_date);
	f_date_fmt = date_fmt(f_date);

	if(i_date_fmt.length > f_date_fmt.length)
		return i_date_fmt;
	else
		return f_date_fmt;
}


// mira si ambos campos tienen bien puesta la fecha en formato YYYYMMDD
function fieldsOk()
{
	var formatsOk = formatOk(i_date) && formatOk(f_date);

	if(!formatsOk)
		return false;

	// min-max
	min_date_sliced = sliceDate_toStr(min_date);
	min_year = min_date_sliced['year'];
	min_month = min_date_sliced['month'];
	min_day = min_date_sliced['day'];

	max_date_sliced = sliceDate_toStr(max_date);
	max_year = max_date_sliced['year'];
	max_month = max_date_sliced['month'];
	max_day = max_date_sliced['day'];

	// initial-final
	i_date_sliced = sliceDate_toStr(i_date);
	i_year = i_date_sliced['year'];
	i_month = i_date_sliced['month'] === '' ? "01" : i_date_sliced['month'];
	i_day = i_date_sliced['day'] === '' ? "01" : i_date_sliced['day'];
	
	f_date_sliced = sliceDate_toStr(f_date);
	f_year = f_date_sliced['year'];
	f_month = f_date_sliced['month'] === '' ? "01" : f_date_sliced['month'];
	f_day = f_date_sliced['day'] === '' ? "01" : f_date_sliced['day'];

	if(i_year + i_month + i_day  >=  f_year + f_month + f_day)
	{
		setErrorBox("La fecha inicial debe ser menor a la final");
		return false;
	}

	fmt = dates_fmt(i_date, f_date);

	switch(fmt)
	{
		case 'YYYY':
		if(i_year < min_year)
		{
			setErrorBox("El año mínimo es " + min_year);
			return false;
		}
		if(f_year > max_year)
		{
			setErrorBox("El año máximo es " + max_year);
			return false;
		}
		break;

		case 'YYYYMM':
		if(i_year + i_month < min_year + min_month)
		{
			setErrorBox("El mes mínimo es " + min_year + min_month);
			return false;
		}
		if(f_year + f_month > max_year + max_month)
		{
			setErrorBox("El mes máximo es " + max_year + max_month);
			return false;
		}
		break;

		case 'YYYYMMDD':
		if(i_year + i_month + i_day < min_year + min_month + min_day)
		{
			setErrorBox("El día mínimo es " + min_date);
			return false;
		}
		if(f_year + f_month + f_day > max_year + max_month + max_day)
		{
			setErrorBox("El día máximo es " + max_date);
			return false;
		}
	}

	$("#error_box").hide();
	return true;
}


// elimina una gráfica
function removeGraph(event)
{
	event.preventDefault();
	var li = $(this).parent();
	li.remove();

	refreshChart();
}


// muestra selectores para dibujar una gráfica
function displayGraphSelector(event)
{
	event.preventDefault();

	var edition =
	"<select name='edition'>" +
	"<option value=''>Edición..</option>" +
	"<option value='ALL'>Todas</option>" +
	"<option value='ES'>ES</option>" +
	"<option value='EN'>EN</option>" +
	"<option value='RU'>RU</option>" +
	"</select>";

	var action =
	"<select name='action'>" +
	"<option value=''>Acción..</option>" +
	"<option value='null'>Visited</option>" +
	"<option value='0'>Edit</option>" +
	"<option value='1'>History</option>" +
	"<option value='2'>Save</option>" +
	"<option value='4'>Search</option>" +
	"</select>";

	var remove = "<a href='#'>[x]</a>";

	var li = "<li>" + edition + action + remove + "</li>";

	var ul = $(this).parent().find("ul");
	ul.append(li);

	// añadimos los eventos al último <li> creado
	li = ul.find("li:last");

	edition = li.find("select[name=edition]");
	edition.on('change', refreshChart);
	action = li.find("select[name=action]");
	action.on('change', refreshChart);

	var remove_link = li.find("a");
	remove_link.on('click', removeGraph);
}



function drawChart(result)
{
	// dibuja todas las gráficas a partir del objeto JSON devuelto, el cual tiene
	// la forma:
	//
	// "{
	//	"dates":
	//		["2013-01-01","2013-01-02","2013-01-03","2013-01-04","2013-01-05",
	//		"2013-01-06","2013-01-07","2013-01-08","2013-01-09","2013-01-10"],
	//
	//	"graphs":
	//	{
	//		"ALL_visited":
	//			["7433","7474","7625","7315","7482","0","0","0","0","0"],
	//		"ALL_saved":
	//			["0","5","4","1","5","0","0","0","0","0"]
	//	}
	// }"

	var dates = result.dates;
	var graphs = result.graphs;

	var data = new google.visualization.DataTable();

	//
	// Esta mierda funciona!
	//
	// data.addColumn('string', 'Country');
	// data.addColumn('number', 'Sales');
	// data.addColumn('number', 'Expenses');
	// data.addRows(4);
	// data.setCell(0, 0, 'US');
	// data.setCell(1, 0, 'CA');
	// data.setCell(2, 0, 'CN');
	// data.setCell(3, 0, 'GB');
	// data.setCell(0, 1, 10000);
	// data.setCell(1, 1, 7000);
	// data.setCell(2, 1, 8000);
	// data.setCell(3, 1, 7000);
	// data.setCell(0, 2, 8000);
	// data.setCell(1, 2, 5000);
	// data.setCell(2, 2, 12000);
	// data.setCell(3, 2, 15000);


	//
	// añadimos columnas
	//
	data.addColumn('string', 'Day');

	// http://stackoverflow.com/questions/684672/loop-through-javascript-object
	for(var graph in graphs)
	{
		if (graphs.hasOwnProperty(graph)) {
			// "ALL_saved -> 0,5,4,1,5,0,0,0,0,0"
			// var i = graph + " -> " + graphs[graph];
			var graph_name = graph;
			// var graph_data = graphs[graph];
			data.addColumn('number', graph_name);
		}
	}


	//
	// añadimos filas
	//
	data.addRows(dates.length);

	var value_num; // posición de cada valor dentro del conjunto de valores de cada gráfica
	var i;

	// primero las fechas
	for(i in dates)
	{
		value_num = parseInt(i, 10);
		data.setCell(value_num, 0, dates[value_num]);
	}

	//luego cada gráfica
	//Empieza en 1 porque ya he pintado la columna para los días.
	//Falta la columna para cada gráfica
	var column_num = 1;

	for(graph in graphs)
	{
		if (graphs.hasOwnProperty(graph))
		{
			value_num = 0;
			// recorremos los datos de la gráfica
			var graph_data = graphs[graph];
			for(i in graph_data)
			{
				value = parseInt(graph_data[i], 10);
				data.setCell(value_num, column_num, value);
				value_num++;
			}
			// "ALL_saved -> 0,5,4,1,5,0,0,0,0,0"
			// var i = graph + " -> " + graphs[graph];
			// var graph_name = graph;
		}
		column_num++;
	}

	var options = {
		title: 'Wikipedia Statistics'
	};

	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	chart.draw(data, options);

	// data.addColumn('number', 'Salary');
	// // data.addColumn('boolean', 'Full Time');
	// data.addRows(3);
	// data.setCell(0, 0, 'ALL_visited');
	// data.setCell(0, 1, 10000);
	// // data.setCell(0, 2, true);
	// data.setCell(1, 0, 'Mary');
	// data.setCell(1, 1, 25000);
	// // data.setCell(1, 2, true);
	// data.setCell(2, 0, 'Steve');
	// data.setCell(2, 1, 8000);
	// data.setCell(2, 2, false);
	// data.setCell(3, 0, 'Ellen');
	// data.setCell(3, 1, 20000);
	// data.setCell(3, 2, true);
	// data.setCell(4, 0, 'Mike');
	// data.setCell(4, 1, 12000);
	// data.setCell(4, 2, false);

	// var data = google.visualization.arrayToDataTable([
	//	['Year', 'Sales', 'Expenses'],
	//	['2004',  2000, 400],
	//	['2005',  1170,      460],
	//	['2006',  660,       1120],
	//	['2007',  1030,      540]
	//	]);
}


function refreshChart()
{
	// dibuja todas las gráficas

	// obtengo las fechas
	i_date = $("#date_selectors input[name=i_date]").val();
	f_date = $("#date_selectors input[name=f_date]").val();

	// comprobamos que las fechas son válidas
	if(!fieldsOk(i_date, f_date))
		return;

	// limpiamos los gráficos para volver a rellenarlo con cada selector
	graphs = [];

	// recorre cada selección de la lista
	// http://stackoverflow.com/questions/2722582/jquery-get-each-divs-sub-child-divs-and-grab-info-into-an-array
	$("#graph_selectors ul li").each(function() {
		var edition = $(this).find("select[name=edition]").val();
		var action = $(this).find("select[name=action]").val();

		if (edition === '' || action === '')
			return;

		// añade la gráfica al array de gráficas
		var graph = {
			edition: edition,
			action: action
		};
		graphs.push(graph);
	});

	// realizamos la petición AJAX si hay algo..
	if(graphs.length !== 0)
	{
		// a enviar en la petición AJAX transformado en objeto JSON
		var chart = {
			i_date: i_date,
			f_date: f_date,
			graphs: graphs
		};

		$.ajax({
			url: 'graph.php',
			type:  'post',
			// data:  { 'chart': chart },
			data: {'chart': JSON.stringify(chart) },
			dataType: 'json',  // esto indica que la respuesta vendrá en formato json
			// cache: false,
			// beforeSend: function () {
			// $("#chart_div").html("Procesando, espere por favor...");
			// },
			success: function(result) {
				drawChart(result);
			}
		});
	}

}