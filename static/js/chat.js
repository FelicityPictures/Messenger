console.log("Chat_ID " + CHAT_ID);

var socket = io();
socket.on('connect', function() {
    socket.emit('join', CHAT_ID)
});
