// Fetch the JSON data
async function fetchFantasyData() {
  try {
    const response = await fetch('processed_fantasy_football_data.json');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

// Create a table for a single game
function createGameTable(gameData, gameNumber) {
  const table = document.createElement('table');
  table.className = 'game-table';
  
  // Create table header
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  ['Home Position', 'Home Player', 'Home Points', 'Away Points', 'Away Player', 'Away Position'].forEach(headerText => {
    const th = document.createElement('th');
    th.textContent = headerText;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Create table body
  const tbody = document.createElement('tbody');
  const maxPlayers = Math.max(gameData.home.players.length, gameData.away.players.length);
  for (let i = 0; i < maxPlayers; i++) {
    const row = document.createElement('tr');
    const homePlayer = gameData.home.players[i] || {};
    const awayPlayer = gameData.away.players[i] || {};
    
    [
      homePlayer.position || '',
      homePlayer.name || '',
      homePlayer.points || '',
      awayPlayer.points || '',
      awayPlayer.name || '',
      awayPlayer.position || ''
    ].forEach(cellText => {
      const td = document.createElement('td');
      td.textContent = cellText;
      row.appendChild(td);
    });
    
    tbody.appendChild(row);
  }
  table.appendChild(tbody);

  // Create total score row
  const totalRow = document.createElement('tr');
  totalRow.className = 'total-score';
  [
    'Total Score',
    '',
    gameData.home.total_score.toFixed(2),
    gameData.away.total_score.toFixed(2),
    '',
    'Total Score'
  ].forEach(cellText => {
    const td = document.createElement('td');
    td.textContent = cellText;
    totalRow.appendChild(td);
  });
  table.appendChild(totalRow);

  return table;
}

// Create a game container
function createGameContainer(gameData, gameNumber) {
  const container = document.createElement('div');
  container.className = 'game-container';
  container.id = `game-${gameNumber}`; // Add unique ID for positioning

  const title = document.createElement('h2');
  title.textContent = `Game ${gameNumber}`;
  container.appendChild(title);

  const teamNames = document.createElement('h3');
  teamNames.textContent = `${gameData.home.team_name} vs ${gameData.away.team_name}`;
  container.appendChild(teamNames);

  const gameTable = createGameTable(gameData, gameNumber);
  container.appendChild(gameTable);

  return container;
}

// Main function to display the data
async function displayFantasyData() {
  const fantasyData = await fetchFantasyData();
  const container = document.getElementById('fantasy-football-data');
  
  if (container) {
    Object.entries(fantasyData).forEach(([gameNumber, gameData]) => {
      const gameContainer = createGameContainer(gameData, gameNumber);
      container.appendChild(gameContainer);
    });
  } else {
    console.error('Container element not found');
  }
}

// Call the main function when the page loads
window.addEventListener('load', displayFantasyData);