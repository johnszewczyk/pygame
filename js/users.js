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

  if (message.type === "user_data_update") {
    updateUnitData(message.data);
  }

};


// FUNCTION: UPDATE PAGE AREA: ENTITY DATA
// -----------------------------------------------------------------------------
function updateUnitData(some_data) {
  const data_list = document.getElementById("user-area");
  data_list.innerHTML = "";

  let current_class_name = null;
  let current_table = null;

  for (const user_data of some_data) {
    if (user_data.type !== current_class_name) {
      // New ClassName encountered, create a new table
      current_class_name = user_data.type;
      current_table = document.createElement("table");
      current_table.id = `table-${current_class_name}`;
      data_list.appendChild(current_table);

      // Add header row to the new table
      const headerRow = current_table.insertRow();
      for (const key of Object.keys(user_data)) {
        const header_cell = headerRow.insertCell();
        header_cell.textContent = key;
        header_cell.className = "header-cell";
      }

    }

    // Add data row to the current table
    const row = current_table.insertRow();
    for (const value of Object.values(user_data)) {
      const cell = row.insertCell();
      cell.textContent = value;
      cell.className = "data";
    }
  }


  // calc & show latency
  CalcLatency(update_start_time);

}


// FUNCTION: LATENCY DISPLAY
// -----------------------------------------------------------------------------

function CalcLatency(update_start_time) {
  const update_end_time = performance.now();
  const latency = update_end_time - update_start_time;
  const latencyDisplay = document.getElementById('latency-display');
  if (latencyDisplay) {
    latencyDisplay.textContent = `Latency: ${latency.toFixed(2)} ms`;
  }
}


// FUNCTION: MAKE TABLE
// -----------------------------------------------------------------------------


// FUNCTION: SEND DATA
// -----------------------------------------------------------------------------

function SendMessageToBackend(message) {
  // Assuming 'ws' is your WebSocket connection object
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(message));
  } else {
    console.error('WebSocket connection is not open. Cannot send message.');
  }
}


