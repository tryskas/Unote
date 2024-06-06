$(document).ready(function() {

    var searchTerm;

     function searchCourses() {
        $.ajax({
            type: "GET",
            url: `/administration/search_course/`,
            data: {
                search_term: searchTerm,
            },
            success: function(data) {
                $("#search-course-results").html(
                data.search_course_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#search-course-form").submit(function(event) {
        event.preventDefault();
        searchTerm = $("#search-course-input").val();
        searchCourses();
    });
});
