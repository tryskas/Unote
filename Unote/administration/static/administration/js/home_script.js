$(document).ready(function() {

// Partie suppression d'utilisateurs-------------------------------------------
    // Intercepter les clics sur les liens du menu
    $('a.menu-link').click(function(event){
        event.preventDefault(); // Empêcher le comportement par défaut du lien
        var url = $(this).attr('href'); // Récupérer l'URL à charger

        // Charger les données depuis l'URL via AJAX
        $.ajax({
            type: 'GET',
            url: url,
            success: function(data){
                // Mettre à jour la zone d'affichage avec les données reçues
                $('#right-panel').html(data);
            }
        });
    });
});
