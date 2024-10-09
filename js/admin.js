// CONNECT TO SERVER - ADMIN
// -----------------------------------------------------------------------------


const ws = hostData.getAdminWebSocket();


// TRACK LATENCY
// -----------------------------------------------------------------------------


let update_start_time = null;


// HANDLE INCOMING DATA
// -----------------------------------------------------------------------------


ws.onmessage = function (event) {
  const message = JSON.parse(event.data);

  // Record the start time
  update_start_time = performance.now();

  if (message.type === "server_data") {
    makeTable("server-data", message.data);
  }

  if (message.type === "game_data") {
    makeTable("game-data", message.data);
  }


  if (message.type === "user_data_update") {
    updatePlayerView(message.data);
  }

  if (message.type === "unit_view_update") {
    updateEntityView(message.data);
  }

  if (message.type === "inst_data") {
    makeTable("inst-data", message.data)
  }


  // track latency - calc & show latency
  calcLatency(update_start_time);


};


// FUNCTION: TWO COLUMN [label] [value] DISPLAY
// -----------------------------------------------------------------------------


function makeTable(some_div, some_data) {
  const data_list = document.getElementById(some_div);
  data_list.innerHTML = ""; // Clear previous data

  for (const [key, value] of Object.entries(some_data)) {
    const row_div = document.createElement("div");
    row_div.classList.add('data-row'); // Add a class for styling

    const label_div = document.createElement("div");
    label_div.textContent = key;
    label_div.classList.add('data-label');

    const value_div = document.createElement("div");
    value_div.textContent = value;
    value_div.classList.add('data-value');

    row_div.appendChild(label_div);
    row_div.appendChild(value_div);
    data_list.appendChild(row_div);
  }
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

const oldGameButton = document.getElementById("old-game-button");
oldGameButton.addEventListener('click', () => {
  // Send a message to the server to trigger oldGame()
  const message = {
    type: "old_game_request"
  };

  // Add visual feedback (optional)
  oldGameButton.classList.add('active');
  setTimeout(function () {
    oldGameButton.classList.remove('active');
  }, 100); // Adjust the duration as needed

  ws.send(JSON.stringify(message));
});

// FUNCTION: UPDATE PAGE AREA: ENTITY VIEW
// -----------------------------------------------------------------------------
function updateEntityView(some_data) {

  // area where unit-view cards will be stacked
  const unit_view_card_stack = document.getElementById("unit-view-area");
  unit_view_card_stack.innerHTML = "";

  for (const unit of some_data) {

    // WRAPPER -  to hold TABLE + CANVAS
    const unit_view_card_wrap = document.createElement("div");
    unit_view_card_wrap.className = "cardwrap";

    // TABLE - make table & set CSS class
    // const unit_table = document.createElement("table");
    // unit_table.className = "unit-info";

    // TABLE - add data to table
    // createRow(unit_table, "Icon:", unit.icon);
    // createRow(unit_table, "Index:", unit.indx);
    // createRow(unit_table, "Moves:", unit.move);

    // CANVAS - make area for canvas & set CSS classs
    const canvas_div = document.createElement("div");
    canvas_div.className = "unit-view-canvas";

    // CANVAS - add unit view canvas
    const canvas = document.createElement("canvas");
    canvas.width = 200;
    canvas.height = 200;
    const ctx = canvas.getContext("2d");
    renderGame(unit.view, ctx, canvas);

    // add canvas to parent div
    canvas_div.appendChild(canvas);

    // wrap the table and canvas
    // unit_view_card_wrap.appendChild(unit_table);
    unit_view_card_wrap.appendChild(canvas_div);

    // add wrap to stack
    unit_view_card_stack.appendChild(unit_view_card_wrap);

  }

}


// FUNCTION: UPDATE PAGE AREA: PLAYER VIEW
// -----------------------------------------------------------------------------
function updatePlayerView(some_data) {

  // area where complete user data "cards" will be stacked
  const user_data_card_stack = document.getElementById("user-list");
  user_data_card_stack.innerHTML = "";


  for (const user of some_data) {

    // WRAPPER -  to hold TABLE + CANVAS
    const user_data_card_wrap = document.createElement("div");
    user_data_card_wrap.className = "cardwrap";

    // make table & set CSS class
    const user_table = document.createElement("table");
    user_table.className = "user-info";


    // Iterate over the user data object keys and values
    for (const [label, data] of Object.entries(user)) {
      if (label !== "view") { // Exclude the "view" data as it's handled separately
        createRow(user_table, label, data);
      }
    }

    // make area for canvas & set CSS classs
    const canvas_div = document.createElement("div");
    canvas_div.className = "user-view-canvas"

    // add user view canvas
    const canvas = document.createElement("canvas");
    canvas.width = 200;
    canvas.height = 200;
    const ctx = canvas.getContext("2d");
    renderGame(user.view, ctx, canvas);

    // add canvas to parent div
    canvas_div.appendChild(canvas);

    // wrap the table and canvas
    user_data_card_wrap.appendChild(user_table);
    user_data_card_wrap.appendChild(canvas_div);

    // add wrap to stack
    user_data_card_stack.appendChild(user_data_card_wrap);
  }

}



// FUNCTION: RENDER GAME
// -----------------------------------------------------------------------------


function renderGame(game_grid, ctx, canvas) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const gride_size = Math.sqrt(game_grid.length);
  const cell_size = Math.min(canvas.width, canvas.height) / gride_size;

  game_grid.forEach((char, i) => {
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


// FUNCTION: LATENCY DISPLAY
// -----------------------------------------------------------------------------


function calcLatency(update_start_time) {
  const update_end_time = performance.now();
  const latency = update_end_time - update_start_time;
  const latency_display = document.getElementById('latency-display');
  if (latency_display) {
    latency_display.textContent = `Latency: ${latency.toFixed(2)} ms`;
  }
}



// FUNCTION: MAKE TABLE
// -----------------------------------------------------------------------------


function createRow(parent_table, label_text, data_text) {
  const row = parent_table.insertRow();  // Create a new row in the table

  const cell_label = row.insertCell();
  cell_label.textContent = label_text;
  cell_label.className = "cell-label";

  const cell_data = row.insertCell();
  cell_data.textContent = data_text;
  cell_data.className = "cell-data";
}
