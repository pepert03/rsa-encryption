const server = Bun.serve({
  // Usamos el puerto que nos dé Render, o el 3000 si estamos en local
  port: process.env.PORT || 3000, 
  // 0.0.0.0 significa "escuchar a todo internet", no solo a localhost
  hostname: "0.0.0.0", 
  
  fetch(req, server) {
    if (server.upgrade(req)) {
      return; 
    }
    return new Response("Servidor P2P Relay funcionando. Conéctate vía WebSocket.");
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