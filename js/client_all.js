// CONNECT TO SERVER - CLIENT
const ws = hostData.getClientWebSocket();


// HANDLE INCOMING DATA
ws.onmessage = function (event) {
  const message = JSON.parse(event.data);

  if (message.type === "gameState") {
    render_game(message.data);

  } else if (message.type === "uptimeUpdate") {
    document.getElementById('uptime').textContent = message.data;

  } else if (message.type === "users_online") {
    document.getElementById('users-online').textContent = message.data;

  }
};


// Get the canvas element and its 2D rendering context
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");


// GFX: vignette effect
// -----------------------------------------------------------------------------

// Create an off-screen canvas for the vignette
const vignetteCanvas = document.createElement('canvas');
vignetteCanvas.width = canvas.width;
vignetteCanvas.height = canvas.height;
const vignetteCtx = vignetteCanvas.getContext("2d");

// Draw the vignette gradient only once on the off-screen canvas
const gradient = vignetteCtx.createRadialGradient(
  vignetteCanvas.width / 2,
  vignetteCanvas.height / 2,
  0,
  vignetteCanvas.width / 2,
  vignetteCanvas.height / 2,
  Math.min(vignetteCanvas.width, vignetteCanvas.height) / 2
);
gradient.addColorStop(0, "rgba(0, 0, 0, 0)");   // Center (transparent)
gradient.addColorStop(0.7, "rgba(0, 0, 0, 0.5)"); // Middle (semi-transparent)
gradient.addColorStop(1, "rgba(0, 0, 0, 1)");   // Edge (black)

vignetteCtx.fillStyle = gradient;
vignetteCtx.fillRect(0, 0, vignetteCanvas.width, vignetteCanvas.height);


// animate on load
uncollapseTV(ctx, 500)
setTimeout(() => {
  animateStatic(ctx, 500); // Start static animation after 500ms (duration of uncollapseTV)
}, 200);


function render_game(gameBoard) {
  // Clear the main canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const grid_size = Math.sqrt(gameBoard.length);
  const cell_size = Math.min(canvas.width, canvas.height) / grid_size;

  // Draw the game board 
  gameBoard.forEach((char, i) => {
    const row = Math.floor(i / grid_size);
    const col = i % grid_size;
    const x = col * cell_size;
    const y = row * cell_size;
    ctx.font = `${cell_size * 0.8}px monospace`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(char, x + cell_size / 2, y + cell_size / 2);
  });

  // Apply the vignette as a mask
  ctx.globalCompositeOperation = "multiply"; // Use multiply for the vignette effect
  ctx.drawImage(vignetteCanvas, 0, 0);
  ctx.globalCompositeOperation = "source-over"; // Reset to default
}


// send user input to the game server
function sendInput(key) {
  ws.send(JSON.stringify({ type: "keypress", data: key }));
};

function handleInput(buttonMap, key) {
  sendInput(key);
  buttonMap[key].classList.add('active');
  setTimeout(function () {
    buttonMap[key].classList.remove('active');
  }, 100);
};




// INPUT BUTTONS
// -----------------------------------------------------------------------------

const buttonMap = {};
document.querySelectorAll("#touch-controls button").forEach(function (button) {
  const key = button.dataset.key.toLowerCase();
  buttonMap[key] = button;

  // Handle button clicks (for desktop)
  button.addEventListener('click', () => {
    handleInput(buttonMap, key);
  });

  // Add mouse event listeners for button press/release (visual feedback)
  // button.addEventListener('mousedown', () => button.classList.add('active'));
  // button.addEventListener('mouseup', () => button.classList.remove('active'));

  // BUTTON - visual feedback
  ['touchend'].forEach(function (type) {
    button.addEventListener(type, function () {
      button.classList.remove('active');
    });
  });

  //Handle button clicks/touches (common for desktop and mobile)  
  // button.addEventListener('click', () => handleInput(buttonMap, key));
  button.addEventListener('touchstart', () => handleInput(buttonMap, key));
}); //End of forEach loop for each button.
