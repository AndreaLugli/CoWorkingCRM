$("#meeting_rooms").change(function() {
	$("#meeting_rooms option:selected").each(function() {
		$("#meeting_rooms_groups").html("");

		val_selected = $( this ).val();
		if(val_selected > 0) {
			show_meeting_rooms(val_selected);
		}
	})
});

function show_meeting_rooms(val) {
	for(i = 1; i <= val; i++) {
		div_to_append = '\
			<div class="form-group">\
				<div class="row">\
					<div class="col-md-5">\
						<input type="text" class="form-control" placeholder="Nome della sala" name="meeting_room_'+i+'" id="meeting_room_'+i+'">\
					</div>\
					<div class="col-md-3">\
						<input type="number" class="form-control" placeholder="Posti" name="seats_room_'+i+'" id="seats_room_'+i+'">\
					</div>\
					<div class="col-md-4">\
						<input type="number" class="form-control" placeholder="Costo per ora" name="price_room_'+i+'" id="price_room_'+i+'">\
					</div>\
				</div>\
			</div>';

		$("#meeting_rooms_groups").append(div_to_append);
	}
}

$("#office_rooms").change(function() {
	$("#office_rooms option:selected").each(function() {
		$("#office_groups").html("");

		val_selected = $( this ).val();
		if(val_selected > 0) {
			show_office(val_selected);
		}
	})
});

function show_office(val) {
	for(i = 1; i <= val; i++) {
		div_to_append = '\
			<div class="form-group">\
				<div class="row">\
					<div class="col-md-6">\
						<input type="text" class="form-control col-md-8" placeholder="Nome dell\'ufficio" name="office_'+i+'" id="office_'+i+'">\
					</div>\
					<div class="col-md-6">\
						<input type="number" class="form-control" placeholder="Posti" name="office_seats_room_'+i+'" id="office_seats_room_'+i+'">\
					</div>\
				</div>\
			</div>';

		$("#office_groups").append(div_to_append);
	}
}
