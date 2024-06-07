$(document).ready(function() {

    var searchTerm;

     function searchUes() {
        $.ajax({
            type: "GET",
            url: `/administration/search_ue/`,
            data: {
                search_term: searchTerm,
            },
            success: function(data) {
                $("#search-ue-results").html(
                data.search_ue_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#search-ue-form").submit(function(event) {
        event.preventDefault();
        searchTerm = $("#search-ue-input").val();
        searchUes();
    });
});
