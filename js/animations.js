function animateStatic(ctx, duration = 500) {
  const startTime = performance.now();

  function drawStatic() {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    for (let i = 0; i < data.length; i += 4) {
      data[i] = data[i + 1] = data[i + 2] = Math.random() * 128;
      data[i + 3] = 255;
    }
    ctx.putImageData(imageData, 0, 0);

    if (performance.now() - startTime < duration) {
      requestAnimationFrame(drawStatic);
    }
  }

  requestAnimationFrame(drawStatic);
}


// fading 

function fadeTransition(ctx, duration = 2000) {
  const startTime = performance.now();

  function fade() {
    const elapsed = performance.now() - startTime;
    const opacity = 1 - Math.min(1, elapsed / duration);
    ctx.globalAlpha = opacity;
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (opacity > 0) {
      requestAnimationFrame(fade);
    } else {
      ctx.globalAlpha = 1; // Reset opacity
    }
  }

  fade(); // Start the fade
}

// flickering

function flickerLights(ctx, flickerInterval = 5000) { // Default to 5 seconds
  function flicker() {
    // Adjust the alpha value for a more subtle flicker
    ctx.fillStyle = `rgba(0, 0, 0, ${Math.random() * 0.3 + 0.1})`;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    setTimeout(flicker, flickerInterval + Math.random() * 2000); // Add some randomness
  }

  flicker();
}


// collapse effect

function collapseTV(ctx, duration = 1000) {
  const startTime = performance.now();
  let topY = 0;
  let bottomY = canvas.height;
  const collapseSpeed = canvas.height / (duration / 16); // Adjust for smoother animation

  function collapseFrame() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the top rectangle
    ctx.fillRect(0, 0, canvas.width, topY);

    // Draw the bottom rectangle
    ctx.fillRect(0, bottomY, canvas.width, canvas.height - bottomY); // Height is dynamic

    // Increase topY and decrease bottomY
    topY += collapseSpeed;
    bottomY -= collapseSpeed;

    // Stop if the rectangles have met in the middle
    if (topY >= bottomY) {
      return;
    }

    // Request the next frame
    requestAnimationFrame(collapseFrame);
  }

  requestAnimationFrame(collapseFrame);
}

function uncollapseTV(ctx, duration = 1000) {
  let topY = canvas.height / 2; // Start from the middle
  let bottomY = canvas.height / 2;
  const collapseSpeed = canvas.height / (duration / 16); // Adjust for smoother animation

  function uncollapseFrame() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the top rectangle
    ctx.fillRect(0, 0, canvas.width, topY);

    // Draw the bottom rectangle
    ctx.fillRect(0, bottomY, canvas.width, canvas.height - bottomY);

    // Decrease topY and increase bottomY
    topY -= collapseSpeed;
    bottomY += collapseSpeed;

    // Stop if fully uncollapsed
    if (topY <= 0) {
      return;
    }

    // Request the next frame
    requestAnimationFrame(uncollapseFrame);
  }

  requestAnimationFrame(uncollapseFrame);
}

function pixelate(ctx, pixelSize = 10) {
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const data = imageData.data;

  for (let y = 0; y < canvas.height; y += pixelSize) {
    for (let x = 0; x < canvas.width; x += pixelSize) {
      const i = (y * canvas.width + x) * 4;
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];

      for (let dy = 0; dy < pixelSize; dy++) {
        for (let dx = 0; dx < pixelSize; dx++) {
          const j = ((y + dy) * canvas.width + (x + dx)) * 4;
          data[j] = r;
          data[j + 1] = g;
          data[j + 2] = b;
        }
      }
    }
  }

  ctx.putImageData(imageData, 0, 0);
}
