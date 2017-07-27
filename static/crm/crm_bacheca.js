$(document).ready(function() {
	$('#summernote').summernote({
		height: "200px",
		callbacks: {
			onImageUpload: function(files) {
				sendFile(files[0]);
				//console.log(editor)
				//console.log(welEditable)
			}
		}
	});


	function sendFile(file) {
		data = new FormData();
		data.append("file", file);
		console.log(data)
		$.ajax({
			data: data,
			type: "POST",
			url: url_send_file,
			cache: false,
			contentType: false,
			processData: false,
			success: function(url) {
				//editor.insertImage(welEditable, url);
				//insertImage
				$('#summernote').summernote('insertImage', url, "pic");
			}
		});

	}
});

