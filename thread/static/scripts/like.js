$("#like-button-btn").on("click", function() {
	let postID = $("#postID").val();
	const postID = $("#postID").val();
	let this_val = $(this);


	$.ajax({
		url: "/like_post",
		data: {
			"postID": postID
		},
		dataType: "json",
		beforeSend: function() {
			//do something
		},
		success: function() {
			//do something
		},
	})
})
