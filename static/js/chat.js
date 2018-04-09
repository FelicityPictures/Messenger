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

socket.on('add_chat_to_list', (data, users_in_chat) => {
  var link ="'/chats/" + data + "'";
  console.log(users_in_chat);
  var user_string = "";
  for (var i = 0; i < users_in_chat.length; i++) {
    user_string = user_string + users_in_chat[i];
  }
  if (!USER_CHATS.includes(data)){
    // $('#chats').append("<a href=" + link +"><li>" + user_string + "</li></a>");
  }
});

socket.on('disconnect', function() {
    socket.emit('leave', CHAT_ID);
});
