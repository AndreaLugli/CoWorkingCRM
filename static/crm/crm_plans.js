$("#tipo").change(function() {
	$("#tipo option:selected").each(function() {
		val_selected = $( this ).val();

		if(val_selected == "PO") {
			id_office = $( this ).attr("data-ufficio");

			$("#office").val(id_office);
		}

		id_location = $( this ).attr("data-location");
		$("#location_id").val(id_location);
	});
});