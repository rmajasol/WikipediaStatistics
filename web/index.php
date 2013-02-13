<?
$title = "Wikipedia Statistics";
require 'includes/header.php';
?> 

<div id="chart_dates">
	<div id="chart_div"></div>

	<div id="error_box"></div>

	<div id="date_selectors">
		<?
		$dates = get_min_max_dates();
		$min_date = $dates['min']['year'] . $dates['min']['month'] 
		. $dates['min']['day'];
		$max_date = $dates['max']['year'] . $dates['max']['month'] 
		. $dates['max']['day'];
		?>
		<input type="text" name="i_date" value="<? echo $min_date; ?>">
		<input type="text" name="f_date" value="<? echo $max_date; ?>">
	</div>
</div>


<div id="graph_selectors">
	<a href="">Add graph</a>
	<ul>
	</ul>
</div>







<?
require 'includes/footer.php';
?>
