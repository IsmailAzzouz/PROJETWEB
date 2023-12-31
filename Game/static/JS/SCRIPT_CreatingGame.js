$(document).ready(function () {
    // Lorsque le bouton "create-game-btn" est cliqué
    $("#create-game-btn").click(function () {
        // Sélectionne le formulaire avec l'id "game-form"
        var form = $("#game-form");

        // Envoie une requête Ajax
        $.ajax({
            type: form.attr("method"),
            url: form.attr("action"),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                // Si la requête est réussie
                if (data.success) {
                    // Redirige vers la page du jeu lors de la connexion réussie
                    window.location.href = url; //url est présent dans le fichier CreatingGame html car django ne passe pas de variable dans du js
                } else {
                    // Gestion des erreurs en cas de problème
                    var errorMessage = '';

                    // Vérifie s'il y a des erreurs liées à "grid_x"
                    if (data.errors.grid_x) {
                        errorMessage += 'Grid X : ' + data.errors.grid_x + '\n' + ' \n';
                    }

                    // Vérifie s'il y a des erreurs liées à "grid_y"
                    if (data.errors.grid_y) {
                        errorMessage += 'Grid Y : ' + data.errors.grid_y + '\n' + ' \n';
                    }

                    // Vérifie s'il y a des erreurs liées à "alignment"
                    if (data.errors.alignment) {
                        errorMessage += 'Alignment : ' + data.errors.alignment + '\n' + ' \n';
                    }
                    if(data.errors.title){
                        errorMessage += 'Game Title : ' + data.errors.title + '\n' + ' \n';
                    }

                    // Affiche un message d'alerte avec les erreurs, le cas échéant
                    if (errorMessage !== '') {
                        alert(errorMessage);
                    } else {
                        // Si aucune erreur spécifique, affiche un message générique
                          alert("Grid X is a required field \nGrid Y is a required field \nAlignment is a required field \nGame Title is a required field");
                    }
                }
            },
            // Gestion des erreurs en cas de problème avec la requête
            // error: function (jqXHR, textStatus, errorThrown) {
            //     // Traitement de la réponse en cas d'erreur
            //     var errorMessage = '';
            //     if (jqXHR.responseJSON.errors.grid_x) {
            //         errorMessage += 'Grid X : ' + jqXHR.responseJSON.errors.grid_x + '\n' + ' \n';
            //     }
            //     if (jqXHR.responseJSON.errors.grid_y) {
            //         errorMessage += 'Grid Y : ' + jqXHR.responseJSON.errors.grid_y + '\n' + ' \n';
            //     }
            //     if (jqXHR.responseJSON.errors.alignment) {
            //         errorMessage += 'Alignment : ' + jqXHR.responseJSON.errors.alignment + '\n' + ' \n';
            //     }
            //     if (errorMessage !== '') {
            //         alert(errorMessage);
            //     } else {
            //         alert("Veuillez écrire quelque chose dans les champs.");
            //     }
            //     console.log(data);
            // }
        });
    });
});

//Commentaires generer par CHATGPT pour plus practiciter