$("#like-button-btn").on("click", function() {
	alert("liked");
    let postID = $("#postID").val();
    let this_val = $(this);

    $.ajax({
        url: "/like_post/",
        type: 'GET',
        data: {
            "postID": postID
        },
        dataType: "json",
        beforeSend: function() {
            // Optionally, disable the button or show a loading indicator
            this_val.prop("disabled", true);
        },
        success: function(response) {
            // Handle success, e.g., update the like count, change the button state
            this_val.prop("disabled", false);
            console.log(response);
        },
        error: function(xhr, status, error) {
            // Handle error, e.g., show an error message
            this_val.prop("disabled", false);
            console.error("Error:", error);
        }
    });
});
