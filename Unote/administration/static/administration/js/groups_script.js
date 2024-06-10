$(document).ready(function() {

    var searchTerm;

     function searchGroups() {
        $.ajax({
            type: "GET",
            url: `/administration/search_group/`,
            data: {
                search_term: searchTerm,
            },
            success: function(data) {
                $("#search-group-results").html(
                data.search_group_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#search-group-form").submit(function(event) {
        event.preventDefault();
        searchTerm = $("#search-group-input").val();
        searchGroups();
    });
});
