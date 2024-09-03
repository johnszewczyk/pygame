// CONNECT TO SERVER - ADMIN
// -----------------------------------------------------------------------------

const ws = hostData.getAdminWebSocket();


// TRACK LATENCY
// -----------------------------------------------------------------------------

let updateStartTime = null;


// CANVAS ELEMENT
// -----------------------------------------------------------------------------

// Get canvas and context
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Set dimensions (adjust as needed)
const grid_size = 10; // Example: 10x10 grid
canvas.width = 3000; // Example: 400 pixels wide
canvas.height = 3000; // Example: 400 pixels tall
let cell_size = Math.min(canvas.width, canvas.height) / grid_size;


// HANDLE INCOMING DATA
// -----------------------------------------------------------------------------

ws.onmessage = function (event) {
  const message = JSON.parse(event.data);

  if (message.type === "framebuffer") {
    // Record the start time
    updateStartTime = performance.now();

    // process data
    renderGame(message.data);
  }

};


// FUNCTIONS - RENDER DATA
// -----------------------------------------------------------------------------

function renderGame(gameBoard) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const grid_size = Math.sqrt(gameBoard.length); // Calculate grid size
  const cell_size = Math.min(canvas.width, canvas.height) / grid_size;

  for (let i = 0; i < gameBoard.length; i++) {
    const row = Math.floor(i / grid_size);
    const col = i % grid_size;

    const x = col * cell_size + cell_size / 2; // Center in cell
    const y = row * cell_size + cell_size / 2; // Center in cell

    ctx.font = `${cell_size * .8}px monospace`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(gameBoard[i], x, y); // Draw the character


    // After the update is complete, calculate and display latency
    const updateEndTime = performance.now();
    const latency = updateEndTime - updateStartTime;
    const latencyDisplay = document.getElementById('latency-display');
    if (latencyDisplay) {
      latencyDisplay.textContent = `Latency: ${latency.toFixed(2)} ms`;
    }


  }
};