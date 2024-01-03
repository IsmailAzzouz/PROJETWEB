
    $(document).ready(function () {
        // Function to check game status
        // Function to check game status
        function checkGameStatus() {
            $.ajax({
                type: 'GET',
                url: 'checkgamestatus/',  // Replace with the actual URL for checking game status
                dataType: 'json',
                success: function (data) {
                    // Check if the game is ready (both players are ready)
                    if (data.ready) {
                        // Make another AJAX request to get player data and game settings
                        $.ajax({
                            type: 'GET',
                            url: 'checkgamestatus/',  // Replace with the actual URL for checking game status (same as the initial request)
                            dataType: 'json',
                            success: function (gameData) {
                                // Redirect to the gamescene page with the received data
                                console.log('Redirect URL:', '/gamescene/player1=' + encodeURIComponent(gameData.player_1) + '/player2=' + encodeURIComponent(gameData.player_2) + '/gamecode=' + encodeURIComponent(gameData.game_idcode) + '/' + encodeURIComponent(gameData.game_private) + '/');
                                window.location.href = '/gamescene/gamecreator=' + encodeURIComponent(gameData.player_1) + '/player2=' + encodeURIComponent(gameData.player_2) + '/gamecode=' + encodeURIComponent(gameData.game_idcode) + '/isgameprivate=' + encodeURIComponent(gameData.game_private) + '/';

                            },
                            error: function (errorData) {
                                console.log('Error getting game scene data:', errorData);
                            }
                        });
                    } else {
                        // Continue checking game status after a delay
                        setTimeout(checkGameStatus, 5000);  // Check every 5 seconds (adjust as needed)
                    }
                },
                error: function (data) {
                    console.log('Error checking game status');
                    console.log(data);
                }
            });
        }

// Call the function to start checking game status
        checkGameStatus();


    });
/**********************************/

