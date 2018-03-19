var sendButton = document.getElementById('sendButton');
var textMessage = document.getElementById('inputText');
sendButton.addEventListener("click", sendMessage);

var socket = io();
socket.on('connect', function() {
  console.log('connected');
});
function sendMessage(){console.log('sending message');
  var messageText = textMessage.value;
  socket.emit('message', messageText);
}
