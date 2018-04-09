console.log("Chat_ID " + CHAT_ID);
console.log("USER_CHATS" + USER_CHATS );
console.log("USER_IN_CHAT"+ USERS_IN_CHAT);

var socket = io();
socket.on('connect', function() {
  socket.emit('join', CHAT_ID);
  if (NEW_CHAT){
    socket.emit('add_chat_to_list', CHAT_ID);
  }
});

socket.on('add_chat_to_list', (data) => {
  console.log("added");
  // $('#chats').append('<li>'+String(data)+'</li><p class="chatMessageUsername">'+username+'</p>')
  $('#chats').append("<a href=" + "/chats/" + CHAT_ID +"<li>" + CHAT_ID + "</li></a>");
});

socket.on('disconnect', function() {
    socket.emit('leave', CHAT_ID);
});
