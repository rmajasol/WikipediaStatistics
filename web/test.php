<?php

require 'functions.php';

$regs = do_query("select * from visited2012");
while($row = mysql_fetch_array($regs))
	echo $row['day'] . ', ' . $row['lang'] . '<br>';
// phpinfo();
?>