var ticks_months = [[1, "Gen"], [2, "Feb"], [3, "Mar"], [4, "Apr"], [5, "Mag"], [6, "Giu"], [7, "Lug"], [8, "Ago"], [9, "Set"], [10, "Ott"], [11, "Nov"], [12, "Dic"]];

var bars_options = {
	show: true,
	barWidth: 0.6,
	fill: true,
	fillColor: {
		colors: [{
			opacity: 0.8
		}, {
			opacity: 0.8
		}]
	}
};

var grid_options = {
	color: "#999999",
	hoverable: true,
	clickable: true,
	tickColor: "#D4D4D4",
	borderWidth: 0
};

$(function() {
	var barOptions = {
		series: {
			bars: bars_options
		},
		xaxis: { 
			ticks: ticks_months 
		},		
		yaxis: {
			tickFormatter: numberWithCommas,
		},			
		colors: ["#1ab394"],
		grid: grid_options,
		legend: {
			show: false
		},
		tooltip: true,
		tooltipOpts: {
			content: "%y"
		}
	};
	
	var barData = {
		data: barchart_val_list
	};

	$.plot($("#flot-bar-chart"), [barData], barOptions);
});


function numberWithCommas(x) {
	return "€" + x.toString().replace(/\B(?=(?:\d{3})+(?!\d))/g, ".");
}


function agregar_pago_mensual(id, amount) {
	$("#invoice_id").val(id);
	$("#register_payment_futuros").modal();

	$("#amount_PAGO").val(amount);
}





$('#data_1 .input-group.date').datepicker({
	todayBtn: "linked",
	keyboardNavigation: false,
	forceParse: false,
	calendarWeeks: true,
	autoclose: true,
	format: 'dd/mm/yyyy',
});





