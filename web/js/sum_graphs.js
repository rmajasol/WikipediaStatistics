//
// handlers para sub_ul
//
function sumGraph_sub_ul_li(event, sub_ul)
{
	// suma a la sub_ul el li anterior
}


function sumGraph_li_sub_ul(event, li)
{
	// suma al li la sub_ul anterior
}


function removeGraph_sub_ul(event, sub_ul)
{
	// elimina todas las gráficas del sub_ul

	var parent_li = sub_ul.parent();
	parent_li.remove();

	refreshChart();
}


function sep_sub_ul(event, parent_li)
{
	// separa todas las gráficas del conjunto sub_ul

	event.preventDefault();

	var next_li = parent_li.next();

	parent_li.find('ul li').each(function(){
		$(this).removeClass("sum");

		//volvemos a mostrar los link para 'sum'
		$(this).find('a.sumGraph_li_li').show();

		// añadimos antes del siguiente li
		next_li.before($(this));

		// tenemos que volver a asignar los eventos a cada li
		addEvents($(this));
	});

	parent_li.remove();
}


//
// handler para sumar gráficas
//
function sumGraph_li_li(event, li)
{
	// suma dos gráficas li

	event.preventDefault();

	// prev_li será la raíz de la lista a sumar..
	var parent_li = li.prev();
	parent_li.addClass('sum');

	var first_li = parent_li.clone();

	// seteamos los selectores en el li clonado
	var first_li_edition_val = parent_li.find('select[name=edition]').val();
	var first_li_action_val = parent_li.find('select[name=action]').val();
	first_li.find('select[name=edition]').val(first_li_edition_val);
	first_li.find('select[name=action]').val(first_li_action_val);

	// añadimos la sub_ul al parent_li
	parent_li.html(
		'<span class="title">Sum:</span><br>' +
		'<ul></ul>'
		);

	// colocamos el contenido antes guardado en un li de la nueva sub_ul
	var sub_ul = parent_li.find('ul');
	sub_ul.append(first_li);
	sub_ul.append(li);
	//añadimos eventos
	addEvents(first_li);
	addEvents(li);
	
	// escondemos el enlace 'sum' de los li de sub_ul
	sub_ul.children().each(function(){
		$(this).find('a.sumGraph_li_li').hide();
	});

	// añadimos enlaces al bloque
	var remove = "<a class='removeGraph_sub_ul' href='#'>[x]</a>";
	var sum = "<a class='sumGraph_sub_ul_li' href='#'>[sum]</a>";
	var sep = "<a class='sep_sub_ul' href='#'>[sep]</a>";
	parent_li.append(sum + sep + remove);

	//
	// agregamos eventos para enlaces del sub_ul
	//
	var remove_link = parent_li.find('a.removeGraph_sub_ul');
	remove_link.on('click', function(e){
		removeGraph_sub_ul(e, parent_li);
	});

	var sum_link = parent_li.find('a.sumGraph_sub_ul_li');
	sum_link.on('click', function(e){
		sumGraph_sub_ul_li(e, parent_li);
	});

	var sep_link = parent_li.find('a.sep_sub_ul');
	sep_link.on('click', function(e){
		sep_sub_ul(e, parent_li);
	});

}