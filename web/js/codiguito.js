// cargamos el paquete para poder pintar las gráficas
google.load("visualization", "1", {packages:["corechart"]});

// para indicarnos si las gráficas ya se han añadido al DOM
var chart_is_visible = false;

// fechas mínima y máxima a poder introducir
var min_date;
var min_date_str;
var max_date;
var max_date_str;

// fechas inicial y final
var i_date;
var f_date;

var i_year;
var i_month;
var f_year;
var f_month;

// conjunto de gráficas como respuesta de la petición AJAX
var graphs = [];

// conjuntos de ediciones, acciones y namespaces
var editions = ['DE', 'EN', 'ES', 'FR', 'IT', 'JA', 'NL', 'PL', 'PT', 'RU'];
var actions = {
	'Visited': 'null',
	'Edit': '0',
	'History': '1',
	'Saved': '2',
	'Search': '4'
};


//
// DOCUMENT READY
//
$(document).on('ready', function(){

	// cuadro de información '#info'
	$( "#info" ).accordion({
		collapsible: true,
		active: false,
		clearstyle: true,
		heightStyle: 'fill'
		// autoHeight: false
		// refresh: true
	});

	min_date = sliceDate_toStr($("#date_selectors input[name=min_date]").val());
	min_date_str = unslice(min_date);
	max_date = sliceDate_toStr($("#date_selectors input[name=max_date]").val());
	max_date_str = unslice(max_date);

	i_date = $("#date_selectors input[name=i_date]").val(min_date['year'] + min_date['month']);
	f_date = $("#date_selectors input[name=f_date]").val(max_date['year'] + max_date['month']);

	var date_selectors = $("#date_selectors input[type=text]");
	date_selectors.on('keyup', refreshChart);

	var add_graph_link = $("#graph_selectors a");
	add_graph_link.on('click', function(e){
		e.preventDefault();
		addGraphSelector();
	});

	addGraphSelector();
	refreshChart();
});


function setErrorBox(msg)
{
	$("#error_box").show();
	$("#error_box").html(msg);
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


function unslice(sliced)
{
	var str = "";
	for(var key in sliced)
		str += sliced[key];

	return str;
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
		setErrorBox(
			"Valid date formats: YYYY, YYYYMM o YYYYMMDD" +
			"<br>Minimum date: " + min_date_str + ", deadline: " + max_date_str
			);
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
	min_year = min_date['year'];
	min_month = min_date['month'];
	min_day = min_date['day'];

	max_year = max_date['year'];
	max_month = max_date['month'];
	max_day = max_date['day'];

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
		setErrorBox("The end date must be greater than the initial");
		return false;
	}

	fmt = dates_fmt(i_date, f_date);

	switch(fmt)
	{
		case 'YYYY':
		if(i_year < min_year)
		{
			setErrorBox("Minimum year: " + min_year);
			return false;
		}
		if(f_year > max_year)
		{
			setErrorBox("Maximum year: " + max_year);
			return false;
		}
		break;

		case 'YYYYMM':
		if(i_year + i_month < min_year + min_month)
		{
			setErrorBox("Minimum month: " + min_year + min_month);
			return false;
		}
		if(f_year + f_month > max_year + max_month)
		{
			setErrorBox("Maximum month: " + max_year + max_month);
			return false;
		}
		break;

		case 'YYYYMMDD':
		if(i_year + i_month + i_day < min_year + min_month + min_day)
		{
			setErrorBox("Minimum day: " + min_year + min_month + min_day);
			return false;
		}
		if(f_year + f_month + f_day > max_year + max_month + max_day)
		{
			setErrorBox("Maximum day: " + max_year + max_month + max_day);
			return false;
		}
	}

	$("#error_box").hide();
	return true;
}


function removeGraph_li(event, li)
{
	// elimina una gráfica

	event.preventDefault();
	li.remove();
	refreshChart();
}


function addToCurrent(li)
{
	// añade eventos a un li de la lista de gráficas

	edition = li.find("select[name=edition]");
	action = li.find("select[name=action]");

	edition.on('change', refreshChart);
	action.on('change', refreshChart);

	// añadimos un shortcut para cuando, teniendo el foco en el selector para action,
	// con sólo pulsar TAB de añadan unos selectores nuevos..
	action.on('keydown', function(e){
		var keyCode = e.keyCode || e.which;

		// keyCode es 9 para la tecla TAB
		if (keyCode == 9) {
			e.preventDefault();

			if(edition.val() !== '' && action.val() !== '')
			{
				refreshChart();
				addGraphSelector();
			}
			else
				edition.focus();
		}
	});

	// si pulsamos la tecla de retroceso estando en algún selector entonces
	// elimina la gráfica anterior
	selector = li.find("select");

	// cuando se trata de pulsar la tecla de retroceso tenemos que especificar
	// keydown en lugar de keyup, ya que por ejemplo en chrome se retrocede
	// a la página anterior al presionar, y no al soltar la tecla
	selector.on('keydown', function(e){
		var keyCode = e.keyCode || e.which;
		if (keyCode == 8) {
			e.preventDefault();
			removeGraph_li(e, li.prev());
		}
	});

	// usando el plugin jquery.hotkeys.js
	// selector.bind('keydown.backspace', function(e){
	// 	var keyCode = e.keyCode || e.which;
	// 	if (keyCode == 8) {
	// 		e.preventDefault();
	// 		// window.history.forward();
	// 		// e.keyCode = 0;
	// 		// e.returnValue = false;
	// 		removeGraph_li(e, li.prev());
	// 	}
	// });
}


function addToPrevious(li)
{
	var remove = "<a class='removeGraph_li' href='#'>x</a>";
	li.append(remove);

	var remove_link = li.find("a.removeGraph_li");
	remove_link.on('click', function(e){
		removeGraph_li(e, li);
	});
}




function addGraphSelector()
{
	// añade los selectores necesarios para dibujar una gráfica

	var edition =
	"<select name='edition'>" +
	"<option value=''>Edition..</option>" +
	"<option value='ALL'>All</option>" +
	"<option value='ALL-EN'>All-EN</option>" +
	"<option value='TOTAL'>Total</option>";
	for(var i in editions)
		edition += "<option value='" + editions[i] + "'>" + editions[i] + "</option>";
	edition += "</select>";

	var action =
	"<select name='action'>" +
	"<option value=''>Action..</option>" +
	"<option value='ALL'>All</option>" +
	"<option value='ALL-Visited'>All-Visited</option>";
	for (var key in actions)
		action += "<option value='" + actions[key] + "'>" + key + "</option>";
	action += "</select>";

	var li = "<li>" + edition + action + "</li>";
	var ul = $('#graph_selectors > ul');
	ul.append(li);

	li = ul.find("li:last");

	// añadimos al <li> actual
	addToCurrent(li);

	// añadimos al <li> anterior
	var li_count = ul.children().length;
	if(li_count > 1)
		addToPrevious(li.prev());

	// ponemos el foco en el nuevo selector
	li.find("select[name=edition]").focus();
}


function drawChart(result)
{
	// dibuja todas las gráficas a partir del objeto JSON devuelto, el cual tiene
	// la forma, por ejemplo para una gráfica pintada en YYYYMMDD (por días):
	//
	// "{
	//	"dates":
	//		["2013-01-01","2013-01-02","2013-01-03","2013-01-04","2013-01-05",
	//		"2013-01-06","2013-01-07","2013-01-08","2013-01-09","2013-01-10"],
	//
	//	"graphs":
	//	{
	//		"TOTAL_visited":
	//			["7433","7474","7625","7315","7482","0","0","0","0","0"],
	//		"TOTAL_saved":
	//			["0","5","4","1","5","0","0","0","0","0"]
	//	}
	// }"


	// si no hay nada mostramos el mensaje 'seleccione al menos una gráfica'
	if(result === null)
	{
		$('#chart_div').remove();
		$('#chart_empty_msg').show();
		chart_is_visible = false;
		return;
	}


	// escondemos el mensaje si hay alguna gráfica por pintar
	$('#chart_empty_msg').hide();
	if(!chart_is_visible)
	{
		$('body').prepend('<div id="chart_div"></div>');
		chart_is_visible = true;
	}

	var dates = result.dates;
	var graphs = result.graphs;

	var data = new google.visualization.DataTable();

	//
	// añadimos columnas
	//
	data.addColumn('string', 'Day');

	// añadimos tantas columnas como gráficas tengamos que pintar
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

	var row_num; // número de fila
	var i;

	// primero las fechas
	for(i in dates)
	{
		row_num = parseInt(i, 10);
		data.setCell(row_num, 0, dates[row_num]);
	}

	// ahora añadimos cada gráfica
	// Empieza en columna 1 porque ya se han pintado todas las fechas
	// (todas las celdas de la columna 0) = eje horizontal completo
	// Falta rellenar la columna para cada gráfica devuelta en la petición AJAX
	var column_num = 1;

	for(graph in graphs)
	{
		if (graphs.hasOwnProperty(graph))
		{
			row_num = 0; // representa el número de fila para la columna 'column_num'

			// recorremos los datos de la gráfica
			var graph_data = graphs[graph];
			for(i in graph_data)
			{
				value = parseInt(graph_data[i], 10);
				data.setCell(row_num, column_num, value);
				row_num++;
			}
			// "ALL_saved -> 0,5,4,1,5,0,0,0,0,0"
			// var i = graph + " -> " + graphs[graph];
			// var graph_name = graph;
		}
		column_num++;
	}

	var options = {
		title: 'Wikipedia Statistics'
		// 'chartArea': {'width': '100%', 'height': '100%'}
		// 'chartArea': {'width': '80%'},
		// 'legend': {'position': 'bottom'}
		// width: '1000px'
	};

	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	chart.draw(data, options);
}


function check_for_disable_options(edition, action)
{
	// -> si edition está en ALL o ALL-EN entonces 'All' en action aparece desactivado
	//
	// -> si action está en ALL entonces ALL y ALL-EN en edition aparecen desactivados
	//
	// http://stackoverflow.com/questions/4610652/jquery-select-option-disabled-if-selected-in-other-select

	var edition_val = edition.val();
	var action_val = action.val();

	if(edition_val === 'ALL' || edition_val === 'ALL-EN')
	{
		action.children("option[value='ALL']").attr('disabled', true);
		action.children("option[value='ALL-Visited']").attr('disabled', true);
	}
	else
	{
		action.children("option[value='ALL']").removeAttr('disabled');
		action.children("option[value='ALL-Visited']").removeAttr('disabled');
	}

	if(action_val === 'ALL' || action_val === 'ALL-Visited')
	{
		edition.children("option[value='ALL']").attr('disabled', true);
		edition.children("option[value='ALL-EN']").attr('disabled', true);
	}
	else
	{
		edition.children("option[value='ALL']").removeAttr('disabled');
		edition.children("option[value='ALL-EN']").removeAttr('disabled');
	}
}


function refreshChart()
{
	// obtengo las fechas
	i_date = $("#date_selectors input[name=i_date]").val();
	f_date = $("#date_selectors input[name=f_date]").val();

	// comprobamos que las fechas son válidas
	if(!fieldsOk(i_date, f_date))
		return;

	// limpiamos los gráficos para volver a rellenarlo con cada selector
	graphs = [];

	//
	// recorre cada selección de la lista
	// http://stackoverflow.com/questions/2722582/jquery-get-each-divs-sub-child-divs-and-grab-info-into-an-array
	$("#graph_selectors li").each(function() {
		var edition = $(this).find("select[name=edition]");
		var action = $(this).find("select[name=action]");

		// en cada par de selectores vemos si hay que desactivar alguna opción
		check_for_disable_options(edition, action);

		edition = edition.val();
		action = action.val();

		if (edition === '' || action === '')
			return;

		//
		// añade la gráfica al array de gráficas
		//
		// si un selector es 'ALL' entonces se pintará todo el conjunto
		//
		var i, key, graph;
		if (edition === 'ALL')
		{
			for(i in editions)
			{
				graph = {
					edition: editions[i],
					action: action
				};
				graphs.push(graph);
			}
		}
		// si se han elegido todas la ediciones menos la inglesa..
		else if (edition === 'ALL-EN')
		{
			for(i in editions)
			{
				if (editions[i] !== 'EN')
				{
					graph = {
						edition: editions[i],
						action: action
					};
					graphs.push(graph);
				}
			}
		}

		if (action === 'ALL')
		{
			for (key in actions)
			{
				graph = {
					edition: edition,
					action: actions[key]
				};
				graphs.push(graph);
			}
		}
		// si se ha elegido pintar todas las acciones para la edición menos Visited..
		else if (action === 'ALL-Visited')
		{
			for (key in actions)
			{
				if (key !== 'Visited')
				{
					graph = {
						edition: edition,
						action: actions[key]
					};
					graphs.push(graph);
				}
			}
		}

		if (edition !== 'ALL' && edition !== 'ALL-EN' &&
			action !== 'ALL' && action !== 'ALL-Visited')
		{
			graph = {
				edition: edition,
				action: action
			};
			graphs.push(graph);
		}
	});

	// si no hay nada que dibujar pues nada..
	if (graphs.length === 0)
	{
		drawChart(result=null);
		return;
	}


	//
	// Si hay alguna gráfica para pintar entonces realizamos la petición AJAX
	// y añadimos nuevos selectores
	//

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