$(document).ready(function() {

    var searchTerm;

     function searchSessions() {
        $.ajax({
            type: "GET",
            url: `/administration/search_session/`,
            data: {
                search_term: searchTerm,
            },
            success: function(data) {
                $("#search-session-results").html(
                data.search_session_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#search-session-form").submit(function(event) {
        event.preventDefault();
        searchTerm = $("#search-session-input").val();
        searchSessions();
    });
});
