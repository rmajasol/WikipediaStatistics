google.load("visualization", "1", {packages:["corechart"]});


var min_date;
var max_date;
var graphs_counter = 0;


var graphs;

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
}


// muestra selectores para dibujar una gráfica
function displayGraphSelector(event)
{
	event.preventDefault();
	graphs_counter++;

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

	var li =
	"<li id='" + graphs_counter + "'>" +
	edition + action + remove +
	"</li>";

	var ul = $(this).parent().find("ul");
	ul.append(li);

	// añadimos los eventos
	li = ul.find("li#" + graphs_counter);

	edition = li.find("select[name=edition]");
	edition.on('change', refreshChart);
	action = li.find("select[name=action]");
	action.on('change', refreshChart);

	var remove_link = li.find("a");
	remove_link.on('click', refreshChart);
}


// añade una gráfica
function getGraph(dates, edition, action)
{

	$.ajax({
		url: 'graph.php',
		data: { "edition": edition, "action": action },
		type:  'post',
		cache: false,
		// beforeSend: function () {
			// $("#chart_div").html("Procesando, espere por favor...");
		// },
		success: function(result) {
			alert(result);
			drawChart();
		}
	});



}


// dibuja todas las gráficas
function refreshChart()
{
	var i_date = $("#date_selectors input[name=i_date]").val();
	var f_date = $("#date_selectors input[name=f_date]").val();

	// comprobamos que las fechas son válidas
	if(!fieldsOk(i_date, f_date))
		return;

	// esta variable contendrá cada gráfica devuelta vía AJAX
	var graphs = [];

	// obtengo las fechas


	// recorre cada selección de la lista
	// http://stackoverflow.com/questions/2722582/jquery-get-each-divs-sub-child-divs-and-grab-info-into-an-array
	// var array = $('#date_selectors ul li').map(function() {
	// var edition = $(this).find("select[name=edition]").val();
	// var action = $(this).find("select[name=action]").val();

	// if (edition === '' || action === '')
	// return;

	// alert("Obteniendo gráfica " + editon + ", " + action + "..");

	// return $(this).val();
	// }).get();


google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);
function drawChart() {
	var data = google.visualization.arrayToDataTable([
		['Year', 'Sales', 'Expenses'],
		['2004',  i,      400],
		['2005',  1170,      460],
		['2006',  660,       1120],
		['2007',  1030,      540]
		]);

	var options = {
		title: 'Company Performance'
	};

	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	chart.draw(data, options);


}
}