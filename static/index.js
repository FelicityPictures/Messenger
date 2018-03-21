var sendButton = document.getElementById('sendButton');
var textMessage = document.getElementById('inputText');
sendButton.addEventListener("click", sendMessage);

var socket = io();
socket.on('connect', function() {
  console.log('connected');
});

// get message
function sendMessage(){console.log('sending message');
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
