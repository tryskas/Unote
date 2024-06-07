$(document).ready(function() {

    var searchTerm;

     function searchRooms() {
        $.ajax({
            type: "GET",
            url: `/administration/search_room/`,
            data: {
                search_term: searchTerm,
            },
            success: function(data) {
                $("#search-room-results").html(
                data.search_room_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#search-room-form").submit(function(event) {
        event.preventDefault();
        searchTerm = $("#search-room-input").val();
        searchRooms();
    });
});
