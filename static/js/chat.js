console.log("Chat_ID " + CHAT_ID);
console.log("USER_CHATS" + USER_CHATS )

var socket = io();
socket.on('connect', function() {
    socket.emit('join', CHAT_ID)
});

socket.on('new_message', (data, chat_id, username, display) => {
  if (display && !(USER_CHATS.find(x => x === chat_id))){
    $('#chats').append("<li>here</li>");
  } else{
    console.log('\nisfound\n');
  }
});
