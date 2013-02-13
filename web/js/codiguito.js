google.load("visualization", "1", {packages:["corechart"]});

var min_date;
var max_date;

// esta variable contendrá cada gráfica devuelta vía AJAX
var graphs = [];
// fechas inicial y final
var i_date;
var f_date;


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


// divide cadena YYYYMMDD en diccionario con año, mes, día
function sliceDate(field)
{
	var year = parseInt(field.substring(0, 4), 10);
	var month = parseInt(field.substring(4, 6), 10);
	var day = parseInt(field.substring(6, 9), 10);

	return {
		year: year,
		month: month,
		day: day
	};
}


// mira si un campo tiene bien puesta la fecha en formato YYYYMMDD
function formatOk(field)
{
	// comprobamos si está bien escrito
	// http://www.9lessons.info/2009/03/perfect-javascript-form-validation.html
	var ok_regexp = /^[0-9]{8}$/;
	field = field.toString();
	if(!ok_regexp.test(field))
	{
		setErrorBox("Introduzca fechas en formato YYYYMMDD");
		return false;
	}

	return true;
}


// mira si ambos campos tienen bien puesta la fecha en formato YYYYMMDD
function fieldsOk(i_date, f_date)
{
	var formatsOk = formatOk(i_date) && formatOk(f_date);
	// var ok = fieldOk(i_date) && fieldOk(f_date);

	if(formatsOk){
		if(i_date < min_date)
		{
			setErrorBox("La fecha mínima es " + min_date);
			return false;
		}
		if(f_date > max_date)
		{
			setErrorBox("La fecha máxima es " + max_date);
			return false;
		}

		$("#error_box").hide();
		return true;
	}
	else
	{
		return false;
	}
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