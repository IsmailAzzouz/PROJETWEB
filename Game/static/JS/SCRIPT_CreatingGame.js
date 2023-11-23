

    $(document).ready(function () {
        $("#create-game-btn").click(function () {
            var form = $("#game-form");
            $.ajax({
                type: form.attr("method"),
                url: form.attr("action"),
                data: form.serialize(),
                dataType: 'json',
                success: function (data) {
                    if (data.success) {
                        // Redirect to the game page upon successful join
                        window.location.href = url;  // Replace with the actual URL for waiting
                    }else{
                        alert("error unkown ligne 16 in jsscript" );
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                // Handle error response


                var errorMessage = '';
                if (jqXHR.responseJSON.errors.grid_x) {
                    errorMessage += 'Grid X: ' + jqXHR.responseJSON.errors.grid_x + '\n' + ' \n';
                }
                if (jqXHR.responseJSON.errors.grid_y) {
                    errorMessage += 'Grid Y: ' + jqXHR.responseJSON.errors.grid_y + '\n'+ ' \n';
                }
                if (jqXHR.responseJSON.errors.alignment) {
                    errorMessage += 'Alignment: ' + jqXHR.responseJSON.errors.alignment + '\n'+ ' \n';
                }
                alert(errorMessage);
            }
            });
        });
    });
