$(document).ready(function() {

    var searchTerm;

     function searchSubjects() {
        $.ajax({
            type: "GET",
            url: `/administration/search_subject/`,
            data: {
                search_term: searchTerm,
            },
            success: function(data) {
                $("#search-subject-results").html(
                data.search_subject_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#search-subject-form").submit(function(event) {
        event.preventDefault();
        searchTerm = $("#search-subject-input").val();
        searchSubjects();
    });
});
