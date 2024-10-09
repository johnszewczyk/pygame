// // FUNCTION: UPDATE PAGE AREA: ENTITY DATA
// // -----------------------------------------------------------------------------


// function updateEntityList(some_data) {
//   const entity_list = document.getElementById("entity-list");
//   entity_list.innerHTML = "";

//   for (const entity of some_data) {
//     const entity_card = document.createElement("div");
//     const entity_table = document.createElement("table");

//     entity_card.className = "entity-card";
//     entity_table.className = "entity-info";
//     entity_list.appendChild(entity_card);
//     entity_card.appendChild(entity_table);

//     // Create tooltip container
//     const tooltip = document.createElement('div');
//     tooltip.className = 'tooltip';

//     createRow(entity_table, entity.icon + entity.serial);

//     // Dynamically create rows based on entity data keys (except some)
//     for (const key in entity) {
//       if (key !== 'icon' && key !== 'serial' && key !== 'view') { // Exclude icon, serial, and xypo
//         createRow(entity_table, key, entity[key]);
//       }
//     }


//     // Modify tooltip to display the EntityView
//     if (entity.view) { // Check if entity has a view
//       const canvas = document.createElement("canvas");
//       canvas.width = 200; // Adjust width as needed
//       canvas.height = 200; // Adjust height as needed
//       const ctx = canvas.getContext("2d");
//       renderGame(entity.view, ctx, canvas);
//       tooltip.appendChild(canvas); // Append the canvas to the tooltip
//     } else {
//       tooltip.textContent = `XY: ${entity.xypo}`; // Default tooltip if no view
//     }

//     entity_card.appendChild(tooltip);


//     // Show tooltip on hover
//     entity_card.addEventListener('mouseover', () => {
//       tooltip.style.display = 'block';
//     });

//     // Hide tooltip on mouseout
//     entity_card.addEventListener('mouseout', () => {
//       tooltip.style.display = 'none';
//     });
//   }


//   // After the update is complete, calculate and display latency
//   const updateEndTime = performance.now();
//   const latency = updateEndTime - update_start_time;
//   console.log(`Entity data update latency: ${latency.toFixed(2)} ms`);
//   const latencyDisplay = document.getElementById('latency-display'); // Assuming you have an element with this ID
//   if (latencyDisplay) {
//     latencyDisplay.textContent = `Latency: ${latency.toFixed(2)} ms`;
//   }

// }






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
