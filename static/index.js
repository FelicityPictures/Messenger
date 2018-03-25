var sendButton = document.getElementById('sendButton');
var textMessage = document.getElementById('inputText');
var messageScroll = document.getElementById("messagesContainer");
var messages = document.getElementById('messages');

//on load, scroll is at the bottom
window.onload = function () {
  messageScroll.scrollTop = messageScroll.scrollHeight;
}

var socket = io();
socket.on('connect', function() {
  console.log('connected');
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
