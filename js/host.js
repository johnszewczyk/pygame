// host.js

// This file holds network settings for all pages by returning either LOCAL or
// REMOTE network configs; e.g., home testing versus running on remote host.

const hostData = (function () {
  let wsClient = null; // WebSocket for clients
  let wsAdmin = null;  // WebSocket for admins

  // LOCAL
  const adminWsUrl = 'ws://localhost:5003';
  const clientWsUrl = 'ws://localhost:5002';

  // REMOTE
  // const adminWsUrl = 'wss://bashgame.online:5003';  
  // const clientWsUrl = 'wss://bashgame.online:5002'; 

  // Functions to get WebSocket instances
  function getClientWebSocket() {
    if (!wsClient) {
      wsClient = new WebSocket(clientWsUrl);
      // (Add client-specific event handlers here)
    }
    return wsClient;
  }

  function getAdminWebSocket() {
    if (!wsAdmin) {
      wsAdmin = new WebSocket(adminWsUrl);
      // (Add admin-specific event handlers here)
    }
    return wsAdmin;
  }

  return { getClientWebSocket, getAdminWebSocket };
})();
