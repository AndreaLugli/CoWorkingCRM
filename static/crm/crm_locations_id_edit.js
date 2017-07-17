/* Meetingroom */

function editar_mr(evt) {
	var node = evt.target || evt.srcElement;

	td_button = $(node);
	td_button_html = td_button.html();
	row_obj = td_button.parent().parent();
	mr_id = row_obj.data("mr");
	all_tds = row_obj.find("td");

	if(td_button_html == "Modifica") {
		td_name = $(all_tds[0]);	
		td_seats = $(all_tds[1]);	
		td_price = $(all_tds[2]);

		td_name_html = td_name.html();
		td_seats_html = td_seats.html();
		td_price_html = td_price.html();

		td_name_input = '<input type="text" class="form-control" value="'+td_name_html+'">';
		td_name.html(td_name_input);

		td_seats_input = '<input type="number" class="form-control" value="'+td_seats_html+'">';
		td_seats.html(td_seats_input);

		td_price_input = '<input type="number" class="form-control" value="'+td_price_html+'">';
		td_price.html(td_price_input);	

		td_button.html("Salva").removeClass("btn-xs");

	}	

	else if (td_button_html == "Salva") {

		all_input = row_obj.find("input");

		new_td_name_html = $(all_input[0]).val();
		new_td_seats_html = $(all_input[1]).val();
		new_td_price_html = $(all_input[2]).val();

		td_name.html(new_td_name_html);
		td_seats.html(new_td_seats_html);
		td_price.html(new_td_price_html);

		td_button.html("Modifica").addClass("btn-xs");
		update_mr(mr_id, new_td_name_html, new_td_seats_html, new_td_price_html);

	}

	else if (td_button_html == "Aggiungi") {

		all_input = row_obj.find("input");

		new_td_name_html = $(all_input[0]).val();
		new_td_seats_html = $(all_input[1]).val();
		new_td_price_html = $(all_input[2]).val();

		td_name = $(all_tds[0]);	
		td_seats = $(all_tds[1]);	
		td_price = $(all_tds[2]);

		td_name.html(new_td_name_html);
		td_seats.html(new_td_seats_html);
		td_price.html(new_td_price_html);

		td_button.html("Modifica").addClass("btn-xs");
		new_mr(new_td_name_html, new_td_seats_html, new_td_price_html);

	}

	else if (td_button_html == "Cancella") {
		confirm_delete_mr(mr_id, row_obj);
	}

}

function confirm_delete_mr(mr_id, row_obj) {
	var r = confirm("Vuoi davvero eliminare la sala riunioni?");

	if (r == true) {
		row_obj.hide();

		delete_mr_url = "/crm/locations/"+location_id+"/edit/mr/"+mr_id+"/delete/";
		$.post(delete_mr_url);
	}
}

function new_mr_row() {

	html_row = '\
		<tr>\
			<td><input type="text" class="form-control" placeholder="Nome della sala"></td>\
			<td><input type="number" class="form-control" placeholder="Posti"></td>\
			<td><input type="number" class="form-control" placeholder="Costo"></td>\
			<td><button type="button" class="btn btn-primary btn-xs">Aggiungi</button></td>\
		</tr>';

	$("#mr_tbody").append(html_row);
}

function new_mr(name, seats, price) {
	update_mr_url = "/crm/locations/"+location_id+"/edit/mr/new/";

	vars = {
		name: name,
		seats: seats,
		price: price
	}

	$.post(update_mr_url, vars);
}

function update_mr(mr_id, name, seats, price) {
	update_mr_url = "/crm/locations/"+location_id+"/edit/mr/" + mr_id + "/";

	vars = {
		name: name,
		seats: seats,
		price: price
	}

	$.post(update_mr_url, vars);
}

function agregar_mr() {
	new_row_html = '\
		<tr>\
			<td><input type="text" class="form-control" placeholder="Name" required></td>\
			<td><input type="number" class="form-control" placeholder="Seats" required></td>\
			<td><input type="number" class="form-control" placeholder="Price" required></td>\
			<td>\
				<button type="button" class="btn btn-primary">Agregar</button>\
			</td>\
		</tr>';

	$("#mr_tbody").append(new_row_html);
}


/* Office */

function editar_off(evt) {
	var node = evt.target || evt.srcElement;

	td_button = $(node);
	td_button_html = td_button.html();
	row_obj = td_button.parent().parent();
	off_id = row_obj.data("off");
	all_tds = row_obj.find("td");

	if(td_button_html == "Modifica") {
		td_name = $(all_tds[0]);	
		td_seats = $(all_tds[1]);	

		td_name_html = td_name.html();
		td_seats_html = td_seats.html();

		td_name_input = '<input type="text" class="form-control" value="'+td_name_html+'">';
		td_name.html(td_name_input);

		td_seats_input = '<input type="number" class="form-control" value="'+td_seats_html+'">';
		td_seats.html(td_seats_input);

		td_button.html("Salva").removeClass("btn-xs");	
	}
	else if (td_button_html == "Salva") {

		all_input = row_obj.find("input");

		new_td_name_html = $(all_input[0]).val();
		new_td_seats_html = $(all_input[1]).val();

		td_name.html(new_td_name_html);
		td_seats.html(new_td_seats_html);

		td_button.html("Modifica").addClass("btn-xs");
		update_off(off_id, new_td_name_html, new_td_seats_html);

	}
	else if (td_button_html == "Aggiungi") {

		all_input = row_obj.find("input");

		new_td_name_html = $(all_input[0]).val();
		new_td_seats_html = $(all_input[1]).val();

		td_name = $(all_tds[0]);	
		td_seats = $(all_tds[1]);	

		td_name.html(new_td_name_html);
		td_seats.html(new_td_seats_html);

		td_button.html("Modifica").addClass("btn-xs");
		new_off(new_td_name_html, new_td_seats_html);

	}	
	else if (td_button_html == "Cancella") {
		confirm_delete_off(off_id, row_obj);
	}	
}

function confirm_delete_off(off_id, row_obj) {
	var r = confirm("Vuoi davvero cancellare l'ufficio?");

	if (r == true) {

		delete_pb_url = "/crm/locations/"+location_id+"/edit/off/"+off_id+"/delete/";

		$.post(delete_pb_url, function(data) {
			row_obj.hide();
		}).fail(function() {
			alert("Non si può eliminare l'ufficio perchè è associato ad un piano");
		})

		
	}	
}

function new_off_row() {

	html_row = '\
		<tr>\
			<td><input type="text" class="form-control" placeholder="Nome" required></td>\
			<td><input type="number" class="form-control" placeholder="Posti" required></td>\
			<td><button type="button" class="btn btn-primary btn-xs">Aggiungi</button></td>\
		</tr>';

	$("#off_tbody").append(html_row);
}

function update_off(off_id, name, seats) {
	update_off_url = "/crm/locations/"+location_id+"/edit/off/" + off_id + "/";

	vars = {
		name: name,
		seats: seats
	}

	$.post(update_off_url, vars);	
}

function new_off(name, seats) {
	new_mr_url = "/crm/locations/"+location_id+"/edit/off/new/";

	vars = {
		name: name,
		seats: seats,
	}

	$.post(new_mr_url, vars);
}
