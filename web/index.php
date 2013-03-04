<?php
require 'includes/header.php';
?>

<div id="chart_empty_msg" class="info_box">Select at least one graph</div><div></div>


<div id="chart_div"></div>



<!-- http://www.w3schools.com/css/css_positioning.asp
An absolute position element is positioned relative to the first parent
element that has a position other than static. If no such element is found,
the containing block is <html> -->
<div class="parent-non-static">

	<div id="graph_selectors" class="box-style1">

		<div id="error_box" class="info_box"></div>

		<div id="date_selectors">
			<input type="text" name="i_date" value=""> -
			<input type="text" name="f_date" value="">

			<!-- Pasaremos la fecha mínima y máxima posible para los datos disponibles -->
			<?php
			$dates = get_min_max_dates();
			$min_date = $dates['min']['year'] . $dates['min']['month']
			. $dates['min']['day'];
			$max_date = $dates['max']['year'] . $dates['max']['month']
			. $dates['max']['day'];
			?>
			<input type="hidden" name="min_date" value="<?php echo $min_date; ?>">
			<input type="hidden" name="max_date" value="<?php echo $max_date; ?>">
		</div>

		<!-- lista de gráficas a pintar -->
		<ul></ul>

		<a href="">Add graph</a>
	</div>

	<div id="info-parent">
		<div id="info">
			<h3>Usage</h3>
			<div>
				<p>
					On this site you can generate graphs based on Wikipedia usage statistics.
					Select a date range and generate as many graphics as you want simultaneously.
				</p>

				<p>
					For example, if we want to see about visits to Spanish wikipedia articles,
					select the 'ES' edition and 'visited' action.
				</p>

				<h1>Tips:</h1>
				<ul>
					<li>When a selector is focused, you only have to type the first
						few letters of your choice.</li>
						<li>You can change date range without losing the already drawed graphs</li>
						<li>You can see the graphs drawn by year, month or day depending on the chosen
							format for dates. From highest to lowest priority, the formats are:
							<ul>
								<li>YYYYMMDD (e.g. 20120525)</li>
								<li>YYYYMM (e.g. 201205)</li>
								<li>YYYY (e.g. 2012)</li>
							</ul>
						</li>
					</ul>

					<h1>Shortcuts:</h1>
					<ul>
						<li><b>TAB</b>: Moves between selectors and draw new graphs</li>
						<li><b>Backspace</b>: Deletes previous graph for the focused selector</li>
					</ul>
				</div>

				<h3>About</h3>
				<div>
					<p>
						WikipediaStatistics is part of a final project for the bachelor's
						degree in Information Systems Engineering.
					</p>
					<p>
						All data shown in the graphs belongs to a MySQL relational database,
						which is updated by an automated script, also made ​​as part of this project,
						using
						<a href="http://sourceforge.net/projects/squilter/" target="blank">WikiSquilter</a> software.
					</p>
					<p>
						You can get the full code on
						<a href="https://github.com/rmajasol/WikipediaStatistics" target="blank">this</a> github repository.
					</p>
				</div>
			</div>
		</div>
	</div>



	<?php
	require 'includes/footer.php';
	?>