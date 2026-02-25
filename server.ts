const server = Bun.serve({
  port: 3000,
  
  fetch(req, server) {
    if (server.upgrade(req)) {
      return; 
    }
    return new Response("P2P relay server running. Connect via WebSocket.");
  },

  websocket: {
    open(ws) {
      console.log("🟢 New client connected");
      ws.subscribe("chat_global"); 
    },

    message(ws, message) {
      console.log("📨 Encrypted packet received, relaying to the network...");
      
      // KEY CHANGE: Use ws.publish instead of server.publish
      // This relays the message to all subscribers in the room,
      // except the sender (more efficient).
      ws.publish("chat_global", message);
    },

    close(ws, code, message) {
      console.log("🔴 Client disconnected");
    },
  },
});

console.log(`🚀 Stable server running at ws://localhost:${server.port}`);