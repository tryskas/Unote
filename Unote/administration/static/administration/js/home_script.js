$(document).ready(function() {
    var ajaxRequest = null;

    // Intercepter les clics sur les liens du menu
    $('a.internal-link').click(function(event) {
        event.preventDefault(); // Empêcher le comportement par défaut du lien

        if (ajaxRequest && ajaxRequest.readyState !== 4) {
            ajaxRequest.abort(); // Annuler la requête AJAX en cours si elle existe
        }

        var url = $(this).attr('href'); // Récupérer l'URL à charger

        // Charger les données depuis l'URL via AJAX
        ajaxRequest = $.ajax({
            type: 'GET',
            url: url,
            success: function(data) {
                // Mettre à jour la zone d'affichage avec les données reçues
                $('#right-panel').html(data);
            }
        });
    });
});
