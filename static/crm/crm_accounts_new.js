$("#type_account").change(function() {
	$("#type_account option:selected").each(function() {
		val_selected = $( this ).val();

		$("#freelancer_row, #company_row").addClass("hidden");

		if(val_selected == "freelancer") {
			$("#freelancer_row").removeClass("hidden");
		}
		else if(val_selected == "company") {
			$("#company_row").removeClass("hidden");
		}
	});
});