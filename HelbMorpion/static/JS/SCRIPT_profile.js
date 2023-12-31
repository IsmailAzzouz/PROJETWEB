 let Profile_select = document.getElementById("profileid").addEventListener("click", showProfile);
        let ModifyProfile_Select = document.getElementById("modifyid").addEventListener("click", showModify);
        let History_Select = document.getElementById("hisotryid").addEventListener("click", showStats);
        let ProfileSection = document.getElementById("Profile");
        let StatsSection = document.getElementById("StatsHistory");
        let ModifySection = document.getElementById("Modify");
        var links = document.querySelectorAll('.Right-navbarr a');

        function showProfile() {
            StatsSection.style.display = "none";
            ModifySection.style.display = "none";
            ProfileSection.style.display = "flex";

        }

        function showModify() {
            StatsSection.style.display = "none";
            ModifySection.style.display = "flex";
            ProfileSection.style.display = "none";
        }

        function showStats() {
            StatsSection.style.display = "flex";
            ModifySection.style.display = "none";
            ProfileSection.style.display = "none";
        }

        ////////////////////////////////////
        const slider = document.querySelector(".items");
        const slides = document.querySelectorAll(".item");
        const button = document.querySelectorAll(".button");

        let current = 0;
        let prev = 4;
        let next = 1;

        for (let i = 0; i < button.length; i++) {
            button[i].addEventListener("click", () => i == 0 ? gotoPrev() : gotoNext());
        }

        const gotoPrev = () => current > 0 ? gotoNum(current - 1) : gotoNum(slides.length - 1);

        const gotoNext = () => current < 4 ? gotoNum(current + 1) : gotoNum(0);

        const gotoNum = number => {
            current = number;
            prev = current - 1;
            next = current + 1;

            for (let i = 0; i < slides.length; i++) {
                slides[i].classList.remove("active");
                slides[i].classList.remove("prev");
                slides[i].classList.remove("next");
            }

            if (next === 5) {
                next = 0;
            }

            if (prev === -1) {
                prev = 4;
            }

            slides[current].classList.add("active");
            slides[prev].classList.add("prev");
            slides[next].classList.add("next");
        }

        //////////////////////////////////////////////

        function filterGames() {
            // Get form data
            var formData = $('#game-filter-form').serialize();

            // Send AJAX request
            $.ajax({
                type: 'POST',
                url: '{% url "filtergames" %}',  // Update the URL to your actual endpoint
                data: formData,
                success: function (response) {
                    console.log(response.games);
                    if (response.success) {
                        // Display filtered games
                        var resultContainer = $('#result-container');
                        resultContainer.empty();  // Clear previous results

                        $.each(response.games, function (index, game) {
                            resultContainer.append('<p>ID Code: ' + game.id_code + ', Winner: ' + game.winner + ', Date: ' + game.game_date + '</p>');
                        });
                    } else {
                        console.error('Error:', response.error);
                    }
                },
                error: function (xhr, status, error) {
                    console.error('AJAX Error:', error);
                }
            });
        }
/*********************************/
        var gamesData = [
            { id_code: 1, grid_x: 10, grid_y: 20, winner: 'Player1', game_date: '2023-01-01' },
            { id_code: 2, grid_x: 15, grid_y: 25, winner: 'Player2', game_date: '2023-01-02' },
            // Add more game data as needed
        ];

        // Aggregate data by day of the week
        var gamesByDay = {};
        gamesData.forEach(function(game) {
            var dayOfWeek = new Date(game.game_date).getDay(); // 0 is Sunday, 1 is Monday, ..., 6 is Saturday
            gamesByDay[dayOfWeek] = (gamesByDay[dayOfWeek] || 0) + 1;
        });

        // Prepare data for the scatter plot
        var scatterData = Object.keys(gamesByDay).map(function(dayOfWeek) {
            return { x: parseInt(dayOfWeek), y: gamesByDay[dayOfWeek] };
        });

        // Create a scatter plot using Chart.js
        var ctx = document.getElementById('gamesScatterPlot').getContext('2d');
        var scatterChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Games Scatter Plot',
                    data: scatterData,
                    backgroundColor: 'rgba(75, 192, 192, 0.5)', // Adjust color as needed
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        ticks: {
                            callback: function(value) {
                                // Convert numeric day of the week to a string
                                var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
                                return days[value];
                            }
                        }
                    },
                    y: {
                        type: 'linear',
                        position: 'left'
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Games played: ' + context.parsed.y;
                            }
                        }
                    }
                }
            }
        });
