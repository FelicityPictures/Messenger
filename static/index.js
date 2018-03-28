var sendButton = document.getElementById('sendButton');
var textMessage = document.getElementById('inputText');
var messageScroll = document.getElementById("messagesContainer");
var messages = document.getElementById('messages');

//on load, scroll is at the bottom
window.onload = function () {
  messageScroll.scrollTop = messageScroll.scrollHeight;
}
console.log("hello");

var socket = io();
socket.on('connect', function() {
    console.log('connected');
});

socket.on('active_user', (username)=>{
  var node = document.createElement("LI");
  var textnode = document.createTextNode(username + "has joined the room");
  node.appendChild(textnode);
  document.getElementById("messages").appendChild(node);
  console.log('active_id: '+ username);
});

socket.on('disconnect', function(){
  console.log('disconnected!');
});

socket.on('deactive_user', (username)=>{
  var node = document.createElement("LI");
  var textnode = document.createTextNode(username + "has left the room");
  node.appendChild(textnode);
  document.getElementById("messages").appendChild(node);
  console.log('deactive_user: '+ username);
});

$("#inputForm").submit((e) => {
  e.preventDefault();
  sendMessage();
})

// get message
function sendMessage(){
  console.log('sending message');
  var messageText = textMessage.value;
  socket.emit('message', messageText);
  document.getElementById("inputText").value = '';
}

// receives messages, displays on the other screen
socket.on('new_message', (data) => {
  var node = document.createElement("LI");
  var textnode = document.createTextNode(data);
  node.appendChild(textnode);
  document.getElementById("messages").appendChild(node);
  console.log("message sent!");
});
