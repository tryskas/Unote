$(document).ready(function() {

    var searchTerm;

     function searchUsers() {
        $.ajax({
            type: "GET",
            url: `/administration/search_user/`,
            data: {
                search_term: searchTerm,
            },
            success: function(data) {
                $("#search-user-results").html(
                data.search_user_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#search-user-form").submit(function(event) {
        event.preventDefault();
        searchTerm = $("#search-user-input").val();
        searchUsers();
    });
});
