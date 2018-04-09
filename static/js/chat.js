console.log("Chat_ID " + CHAT_ID);
console.log("USER_CHATS" + USER_CHATS )

var socket = io();
socket.on('connect', function() {
    socket.emit('join', CHAT_ID)
});
