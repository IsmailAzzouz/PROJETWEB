 $(document).ready(function () {
        $("#join-game-btn").click(function () {
            var gameCode = $("#game-code").val();

            // Get the CSRF token from the cookie
            var csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];

            $.ajax({
                type: 'POST',
                url: url_joining,  // Replace with the actual URL for joining a game
                data: {game_code: gameCode},
                dataType: 'json',
                headers: {"X-CSRFToken": csrftoken},  // Include the CSRF token in the headers
                success: function (data) {
                    if (data.success) {
                        // Redirect to the game page upon successful join
                        window.location.href = url_waiting;  // Replace with the actual URL for waiting
                    } else {
                        // Handle errors (e.g., display error messages)
                        alert('Error: '+ data.message);
                        console.log(data.message);
                        console.log(data);
                    }
                },
                error: function (data) {
                    alert("Error : Game doesn't exist" + data.message);
                    console.log(data);
                }
            });
        });
    });
