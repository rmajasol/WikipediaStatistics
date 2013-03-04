def is_rel(route):
	"""
	Indica si la ruta que introducimos es relativa o no
	"""

	m = re.match("/\/(.*)\/.*", os.path.abspath('.'))
	root_path = os.path.abspath('.')
		# seteamos txt_year con el año del dumped.txt
		global txt_year
		txt_year = m.group(1)
	return route[:]