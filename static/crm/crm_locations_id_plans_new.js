$("#type_of_membership").change(function() {
	$("#type_of_membership option:selected").each(function() {
		val_selected = $( this ).val();
		$("#meeting_room_hours_div").show();
		if(val_selected == "PO") {
			$("#offices").show();
		}
		else {
			$("#offices").hide();
		}

	})
});