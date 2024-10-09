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

  // track latency - start time
  update_start_time = performance.now();

  if (message.type === "tile_data_update") {
    updateTileData(message.data);
  }

  // track latency - calc & show latency
  CalcLatency(update_start_time);


}


// PAGE AREA: DATA SELECTOR CHECKBOXES
// -----------------------------------------------------------------------------

const tileFilters = document.querySelectorAll('.tile-filter'); // Select the new tile-filter elements

tileFilters.forEach(filter => {
  filter.addEventListener('click', () => {
    filter.classList.toggle('active'); // Toggle the 'active' class
    const tileType = filter.dataset.filter;

    // Capitalize the first letter to match the class name
    const tileClassName = tileType.charAt(0).toUpperCase() + tileType.slice(1) + 'Tile';

    SendMessageToBackend({
      type: 'toggle_tile_type',
      tile_type: tileClassName, // Send the class name
      enabled: filter.classList.contains('active') // Check if the 'active' class is present
    });
  });
});


// FUNCTION: LATENCY DISPLAY
// -----------------------------------------------------------------------------

function updateTileData(some_data) {
  const data_list = document.getElementById("tile-area");
  data_list.innerHTML = ""; // Clear previous content

  let current_class_name = null;
  let current_table = null;

  for (const tile_data of some_data) {
    if (tile_data.type !== current_class_name) {
      // New ClassName, create new table 
      current_class_name = tile_data.type;
      current_table = document.createElement("table");
      current_table.id = `table-${current_class_name}`;
      data_list.appendChild(current_table);

      // Add header row
      const headerRow = current_table.insertRow();
      for (const key of Object.keys(tile_data)) {
        const header_cell = headerRow.insertCell();
        header_cell.textContent = key;
        header_cell.className = "header-cell";
      }
    }

    // Add data row, make the first cell a link
    const row = current_table.insertRow();
    let firstCell = true;
    for (const value of Object.values(tile_data)) {
      const cell = row.insertCell();
      if (firstCell) {
        // Make the first cell a link
        const link = document.createElement('a');
        link.href = `/tile_details?tile_id=${tile_data.id}`; // Assuming you have a 'tile_details' route
        link.textContent = value;
        cell.appendChild(link);
        firstCell = false;
      } else {
        cell.textContent = value;
      }
      cell.className = "data";
    }
  }
}

// FUNCTION: LATENCY DISPLAY
// -----------------------------------------------------------------------------

function CalcLatency(update_start_time) {
  const update_end_time = performance.now();
  const latency = update_end_time - update_start_time;
  const latency_display = document.getElementById('latency-display');
  if (latency_display) {
    latency_display.textContent = `Latency: ${latency.toFixed(2)} ms`;
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
