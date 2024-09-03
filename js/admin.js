// CONNECT TO SERVER - ADMIN
// -----------------------------------------------------------------------------

const ws = hostData.getAdminWebSocket();

// TRACK LATENCY
// -----------------------------------------------------------------------------

let updateStartTime = null;

// HANDLE INCOMING DATA
// -----------------------------------------------------------------------------

ws.onmessage = function (event) {
  const message = JSON.parse(event.data);

  // Record the start time
  updateStartTime = performance.now();

  if (message.type === "server_data") {
    updateServerData(message.data);
  }

  if (message.type === "game_data") {
    updateGameData(message.data);
  }

  if (message.type === "player_data_update") {
    updatePlayerView(message.data);
  }

  if (message.type === "entity_view_update") {
    updateEntityView(message.data);
  }

  if (message.type === "entity_data_update") {

    updateEntityList(message.data);
  }

};


// FUNCTION: UPDATE PAGE AREA: SERVER DATA
// -----------------------------------------------------------------------------

function updateServerData(some_data) {
  const data_list = document.getElementById("server-data");
  data_list.innerHTML = ""; // Clear previous data

  // make table
  const data_table = document.createElement("table");

  // draw data 
  for (const [key, value] of Object.entries(some_data)) {
    createRow(data_table, key, value);
  }

  data_list.appendChild(data_table);
}

// FUNCTION: UPDATE PAGE AREA: SERVER DATA: GAME DATA
// -----------------------------------------------------------------------------

function updateGameData(some_data) {
  const data_list = document.getElementById("game-data")
  data_list.innerHTML = "";

  // make table
  const data_table = document.createElement("table");

  // draw data 
  for (const [key, value] of Object.entries(some_data)) {
    createRow(data_table, key, value);
  }

  data_list.appendChild(data_table);


}

// PAGE AREA: CONTROL PANEL
// -----------------------------------------------------------------------------
const newGameButton = document.getElementById("new-game-button");
newGameButton.addEventListener('click', () => {
  // Send a message to the server to trigger newGame()
  const message = {
    type: "new_game_request"
  };

  // Add visual feedback (optional)
  newGameButton.classList.add('active');
  setTimeout(function () {
    newGameButton.classList.remove('active');
  }, 100); // Adjust the duration as needed

  ws.send(JSON.stringify(message));
});


// FUNCTION: UPDATE PAGE AREA: ENTITY DATA
// -----------------------------------------------------------------------------
function updateEntityList(some_data) {
  const entity_list = document.getElementById("entity-list");
  entity_list.innerHTML = "";

  for (const entity of some_data) {
    const entity_card = document.createElement("div");
    const entity_table = document.createElement("table");

    entity_card.className = "entity-card";
    entity_table.className = "entity-info";
    entity_list.appendChild(entity_card);
    entity_card.appendChild(entity_table);

    // Create tooltip container
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';

    createRow(entity_table, entity.icon + entity.serial);

    // Dynamically create rows based on entity data keys (except some)
    for (const key in entity) {
      if (key !== 'icon' && key !== 'serial' && key !== 'view') { // Exclude icon, serial, and xypo
        createRow(entity_table, key, entity[key]);
      }
    }


    // Modify tooltip to display the EntityView
    if (entity.view) { // Check if entity has a view
      const canvas = document.createElement("canvas");
      canvas.width = 200; // Adjust width as needed
      canvas.height = 200; // Adjust height as needed
      const ctx = canvas.getContext("2d");
      renderGame(entity.view, ctx, canvas);
      tooltip.appendChild(canvas); // Append the canvas to the tooltip
    } else {
      tooltip.textContent = `XY: ${entity.xypo}`; // Default tooltip if no view
    }

    entity_card.appendChild(tooltip);


    // Show tooltip on hover
    entity_card.addEventListener('mouseover', () => {
      tooltip.style.display = 'block';
    });

    // Hide tooltip on mouseout
    entity_card.addEventListener('mouseout', () => {
      tooltip.style.display = 'none';
    });
  }


  // After the update is complete, calculate and display latency
  const updateEndTime = performance.now();
  const latency = updateEndTime - updateStartTime;
  console.log(`Entity data update latency: ${latency.toFixed(2)} ms`);
  const latencyDisplay = document.getElementById('latency-display'); // Assuming you have an element with this ID
  if (latencyDisplay) {
    latencyDisplay.textContent = `Latency: ${latency.toFixed(2)} ms`;
  }

}





// FUNCTION: UPDATE PAGE AREA: ENTITY VIEW
// -----------------------------------------------------------------------------
function updateEntityView(some_data) {

  // area where entity-view cards will be stacked
  const entity_view_card_stack = document.getElementById("entity-view-area");
  entity_view_card_stack.innerHTML = "";

  for (const entity of some_data) {

    // WRAPPER -  to hold TABLE + CANVAS
    const entity_view_card_wrap = document.createElement("div");
    entity_view_card_wrap.className = "cardwrap";

    // TABLE - make table & set CSS class
    // const entity_table = document.createElement("table");
    // entity_table.className = "entity-info";

    // TABLE - add data to table
    // createRow(entity_table, "Icon:", entity.icon);
    // createRow(entity_table, "Index:", entity.indx);
    // createRow(entity_table, "Moves:", entity.move);

    // CANVAS - make area for canvas & set CSS classs
    const canvas_div = document.createElement("div");
    canvas_div.className = "entity-view-canvas";

    // CANVAS - add entity view canvas
    const canvas = document.createElement("canvas");
    canvas.width = 200;
    canvas.height = 200;
    const ctx = canvas.getContext("2d");
    renderGame(entity.view, ctx, canvas);

    // add canvas to parent div
    canvas_div.appendChild(canvas);

    // wrap the table and canvas
    // entity_view_card_wrap.appendChild(entity_table);
    entity_view_card_wrap.appendChild(canvas_div);

    // add wrap to stack
    entity_view_card_stack.appendChild(entity_view_card_wrap);

  }

}


// FUNCTION: UPDATE PAGE AREA: PLAYER VIEW
// -----------------------------------------------------------------------------
function updatePlayerView(some_data) {

  // area where complete player data "cards" will be stacked
  const player_data_card_stack = document.getElementById("player-list");
  player_data_card_stack.innerHTML = "";


  for (const player of some_data) {

    // WRAPPER -  to hold TABLE + CANVAS
    const player_data_card_wrap = document.createElement("div");
    player_data_card_wrap.className = "cardwrap";

    // make table & set CSS class
    const player_table = document.createElement("table");
    player_table.className = "player-info";

    // add data to table
    // createRow(player_table, "Icon:", player.icon);
    // createRow(player_table, "Addr:", player.addr);
    // createRow(player_table, "Time:", player.time);
    // createRow(player_table, "Index:", player.indx);
    // createRow(player_table, "Moves:", player.move);

    // Iterate over the player data object keys and values
    for (const [label, data] of Object.entries(player)) {
      if (label !== "view") { // Exclude the "view" data as it's handled separately
        createRow(player_table, label, data);
      }
    }

    // make area for canvas & set CSS classs
    const canvas_div = document.createElement("div");
    canvas_div.className = "player-view-canvas"

    // add player view canvas
    const canvas = document.createElement("canvas");
    canvas.width = 200;
    canvas.height = 200;
    const ctx = canvas.getContext("2d");
    renderGame(player.view, ctx, canvas);

    // add canvas to parent div
    canvas_div.appendChild(canvas);

    // wrap the table and canvas
    player_data_card_wrap.appendChild(player_table);
    player_data_card_wrap.appendChild(canvas_div);

    // add wrap to stack
    player_data_card_stack.appendChild(player_data_card_wrap);
  }

}

// FUNCTION: MAKE TABLE
// -----------------------------------------------------------------------------

function createRow(parent_table, label_text, data_text) {
  const row = parent_table.insertRow();  // Create a new row in the table

  const label_cell = row.insertCell();
  label_cell.textContent = label_text;
  label_cell.className = "player-label";

  const data_cell = row.insertCell();
  data_cell.textContent = data_text;
  data_cell.className = "player-data";
}


// FUNCTION: RENDER GAME
// -----------------------------------------------------------------------------

function renderGame(gameBoard, ctx, canvas) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const gride_size = Math.sqrt(gameBoard.length);
  const cell_size = Math.min(canvas.width, canvas.height) / gride_size;

  gameBoard.forEach((char, i) => {
    const row = Math.floor(i / gride_size);
    const col = i % gride_size;
    const x = col * cell_size;
    const y = row * cell_size;
    ctx.font = `${cell_size * 0.8}px monospace`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(char, x + cell_size / 2, y + cell_size / 2);
  });
}