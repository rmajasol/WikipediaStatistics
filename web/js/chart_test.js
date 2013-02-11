// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(
		// Callback that creates and populates a data table,
		// instantiates the pie chart, passes in the data and
		// draws it.
		function(){
			// Create the data table.
			var data = new google.visualization.DataTable();
			
			data.addColumn('string', 'Topping');
			data.addRows(['Mushrooms', 'Onions', 'Olives', 'Zucchini', 'Pepperoni']);

			data.addColumn('number', 'Slices');
			data.addRows([3, 1, 1, 1, 2]);

			// Set chart options
			var options = {
				'title':'Wikipedia Statistics',
				'width':800,
				'height':600
			};

			// Instantiate and draw our chart, passing in some options.
			var chart = new google.visualization.LineChart($('#chart_div'));
			chart.draw(data, options);
		});


// 	// Create the data table.
	// 	var data = new google.visualization.DataTable();

	// 	data.addColumn('string', 'Topping');
	// 	data.addRows(['Mushrooms', 'Onions', 'Olives', 'Zucchini', 'Pepperoni']);

	// 	data.addColumn('number', 'Slices');
	// 	data.addRows([3, 1, 1, 1, 2]);

	// 	// Set chart options
	// 	var options = { 'title':'Wikipedia Statistics' };

	// 	// Instantiate and draw our chart, passing in some options.
	// 	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	// 	chart.draw(data, options);
	// }


function draw()
{
	var data = google.visualization.arrayToDataTable([
		['Year', 'Sales', 'Expenses'],
		['2004',  10,      400],
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


function draw2()
{
	var data = google.visualization.arrayToDataTable([
		['Year', 'Sales', 'Expenses'],
		['2004',  10,      400],
		['2005',  1170,      460]
		]);

	var options = {
		title: 'Company Performance'
	};

	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
	chart.draw(data, options);
}


$(document).on('ready', function(){
	draw();

	var dos = "hola";

	$("body").on('keyup', draw2);
});