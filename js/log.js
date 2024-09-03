// CONNECT TO SERVER - ADMIN
const ws = hostData.getAdminWebSocket();

// HANDLE INCOMING DATA
ws.onmessage = function (event) {
  const data = JSON.parse(event.data);

  // HANDLE LOG - GAME
  if (data.type === "log_data") {
    // Loop through log entries and add to the page

    // wipe last
    const log_area = document.getElementById("log-data");
    log_area.innerHTML = "";

    // draw data
    for (const logEntry of data.data) {
      updateLogData(logEntry);
    }
  }


  if (data.type === "net_data") {
    const net_area = document.getElementById("net-data");
    net_area.innerHTML = "";

    for (const logEntry of data.data) {
      updateNetData(logEntry);
    }
  }

};


// FORMAT DATA - GAME LOG
function updateLogData(message) {
  const log_area = document.getElementById("log-data");
  const log_item_div = document.createElement("div");
  log_item_div.className = "log-item";
  log_item_div.textContent = message;
  log_area.appendChild(log_item_div);
}


// FORMAT DATA - NETWORK LOG
function updateNetData(message) {
  const net_area = document.getElementById("net-data");
  const log_item_div = document.createElement("div");
  log_item_div.className = "log-item";

  // Format the log entry text
  const entryText = `${message.ADDR}:${message.PORT}`;
  log_item_div.textContent = entryText;
  net_area.appendChild(log_item_div);
}


