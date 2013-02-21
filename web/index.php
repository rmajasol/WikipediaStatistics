<?
require 'includes/header.php';
?> 

<div id="chart_empty_msg" class="info_box">Seleccione al menos una gráfica</div><div></div>

<div id="chart_div"></div>


<div id="graph_selectors">
	<div id="error_box" class="info_box"></div>

	<div id="date_selectors">
		<input type="text" name="i_date" value=""> - 
		<input type="text" name="f_date" value="">

		<!-- Pasaremos la fecha mínima y máxima posible para los datos disponibles -->
		<?
		$dates = get_min_max_dates();
		$min_date = $dates['min']['year'] . $dates['min']['month'] 
		. $dates['min']['day'];
		$max_date = $dates['max']['year'] . $dates['max']['month'] 
		. $dates['max']['day'];
		?>
		<input type="hidden" name="min_date" value="<? echo $min_date; ?>">
		<input type="hidden" name="max_date" value="<? echo $max_date; ?>">
	</div>

	<!-- lista de gráficas a pintar -->
	<ul></ul>
	
	<a href="">Add graph</a>
</div>


<?
require 'includes/footer.php';
?>
