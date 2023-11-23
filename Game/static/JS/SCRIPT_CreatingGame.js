

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
                    } else {
                        // Handle errors (e.g., display error messages)
                        console.log('Error joining the game:', data.message);
                    }
                },
                error: function (data) {
                    // Handle error response
                    alert("Veuillez remplire TOUT les champs");
                    console.log(data);

                }
            });
        });
    });
