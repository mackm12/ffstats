// Team logo URL function
function getTeamLogoURL(teamId) {
    return `https://a.espncdn.com/i/teamlogos/ncaa/500/${teamId}.png`;
}

// Iowa's team ID
const IOWA_TEAM_ID = 2294;

// Mapping of team names to ESPN IDs
const teamIdMap = {
    "Northern Illinois Huskies": 2459,
    "Virginia Tech Hokies": 259,
    "Toledo Rockets": 2649,
    "Drake Bulldogs": 2181,
    "Kansas Jayhawks": 2305,
    "Washington State Cougars": 265,
    "Rhode Island Rams": 227,
    "BYU Cougars": 252,
    "Tennessee Lady Volunteers": 2633,
    "Iowa State Cyclones": 66,
    "Michigan State Spartans": 127,
    "Northern Iowa Panthers": 2460,
    "Purdue Boilermakers": 2509,
    "Penn State Lady Lions": 213,
    "Maryland Terrapins": 120,
    "Illinois Fighting Illini": 356,
    "Indiana Hoosiers": 84,
    "Nebraska Cornhuskers": 158,
    "Oregon Ducks": 2483,
    "Washington Huskies": 264,
    "Northwestern Wildcats": 77,
    "USC Trojans": 30,
    "Minnesota Golden Gophers": 135,
    "Rutgers Scarlet Knights": 164,
    "Ohio State Buckeyes": 194,
    "UCLA Bruins": 26,
    "Michigan Wolverines": 130,
    "Wisconsin Badgers": 275
};

// Function to format date and time
function formatDateTime(dateString, timeString) {
    const date = new Date(dateString + 'T' + timeString + ':00Z');
    const formattedDate = date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
    const formattedTime = date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    return { formattedDate, formattedTime };
}

// Function to display a single game
function displayGame(game, gameId) {
    const scheduleContainer = document.getElementById('schedule-container');
    scheduleContainer.innerHTML = ''; // Clear existing content
    
    const { formattedDate, formattedTime } = formatDateTime(game.date, game.time);
    const gameElement = document.createElement('div');
    gameElement.className = 'game';
    gameElement.setAttribute('data-game-id', gameId);
    
    const opponentId = teamIdMap[game.opponent] || 'unknown';
    
    gameElement.innerHTML = `
        <h2>Next Upcoming Game</h2>
        <p><strong>Date:</strong> ${formattedDate}</p>
        <p><strong>Time:</strong> ${formattedTime}</p>
        <div class="teams">
            <span class="team">
                <img src="${getTeamLogoURL(IOWA_TEAM_ID)}" alt="Iowa Hawkeyes" class="team-logo">
                Iowa Hawkeyes
            </span>
            vs
            <span class="team">
                <img src="${getTeamLogoURL(opponentId)}" alt="${game.opponent}" class="team-logo">
                ${game.opponent}
            </span>
        </div>
        <p><strong>Location:</strong> ${game.venue}</p>
    `;
    scheduleContainer.appendChild(gameElement);
}

// Function to find and display the next upcoming game
function displayNextGame(scheduleData) {
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Set to beginning of day for accurate comparison

    let nextGame = null;
    let nextGameId = null;

    for (let i = 0; i < scheduleData.length; i++) {
        const gameDate = new Date(scheduleData[i].date);
        if (gameDate >= today) {
            nextGame = scheduleData[i];
            nextGameId = i + 1; // Game IDs start from 1
            break;
        }
    }

    if (nextGame) {
        displayGame(nextGame, nextGameId);
    } else {
        const scheduleContainer = document.getElementById('schedule-container');
        scheduleContainer.innerHTML = '<p>No upcoming games scheduled.</p>';
    }
}

// Fetch and display the next game
fetch('iowa_womens_basketball_schedule_2025.json')
    .then(response => response.json())
    .then(data => {
        displayNextGame(data);
    })
    .catch(error => {
        console.error('Error loading the schedule:', error);
        const scheduleContainer = document.getElementById('schedule-container');
        scheduleContainer.innerHTML = '<p>Error loading schedule. Please try again later.</p>';
    });