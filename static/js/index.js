console.log("Chat_ID " + CHAT_ID)


function scrollToBottomOfMessages(){
  var messageScroll = $('#messagesContainer');
  messageScroll.scrollTop(messageScroll.prop("scrollHeight"));
}

// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// YAS OKAY THIS IS THE SOCKET SHITS, GO BELOW TO SEE THE LOADING THE PAGE SHITS
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
var socket = io();
socket.on('connect', function() {
    console.log('connected');
    socket.emit('join', CHAT_ID)
});

socket.on('active_user', (username)=>{
  // var node = document.createElement("LI");
  var textnode = document.createTextNode(username + "has joined the room");
  // node.append(textnode);
  $('#messages').append('<li>'+username+' joined the room</li>');
  scrollToBottomOfMessages();
  console.log('active_id: '+ username);
});

socket.on('disconnect', function(){
  console.log('disconnected!');
});

socket.on('deactive_user', (username)=>{
  // var node = document.createElement("LI");
  var textnode = document.createTextNode(username + " has left the room");
  // node.appendChild(textnode);
  // $('#messages').append(node);
  $('#messages').append('<li>'+username+' has left the room.</li>');
  scrollToBottomOfMessages();
  console.log('deactive_user: '+ username);
});

$("#inputForm").submit((e) => {
  e.preventDefault();
  sendMessage();
})

// get message
function sendMessage(){
  console.log('sending message');
  var textMessage = $('#inputText');
  var messageText = textMessage.val();
  console.log(messageText);
  socket.emit('message', messageText, CHAT_ID);
  $("#inputText").val('');
}

// receives messages, displays on the other screen
socket.on('new_message', (data, chat_id) => {
  console.log("heres");
  $('#messages').append('<li>'+String(data)+'</li>');
  scrollToBottomOfMessages();
  console.log("message sent to" + String(chat_id) + "!");
});

// logout button
$('#logout').click(function(){
  window.location.href = '../logout';
});

// compose button
$('#compose').click(function(){
  $('#chatBox').hide();
  $('#newChatBox').show();
  // window.location.href = '../new_chat';
});

var lastClicked = $('#selectViewActives');
var currentWindow = $('#activeUsers');
// select window >
// Should change to different windows when clicked
// Need window specific functions
function toggleSelected(elementClicked){
  lastClicked.toggleClass('selected');
  elementClicked.toggleClass('selected');
  lastClicked = elementClicked;
};
$('#selectExistingConvos').click(function(){
  toggleSelected($(this));
  currentWindow.hide();
  $('#chats').show();
  currentWindow = $('#chats');
  // load or show existing conversations
});
$('#selectViewActives').click(function(){
  toggleSelected($(this));
  currentWindow.hide();
  $('#activeUsers').show();
  currentWindow = $('#activeUsers');
});
$('#selectGames').click(function(){
  toggleSelected($(this));
  // load or show games
});

$('#chats').hide();
$('#newChatBox').hide();

//on load, scroll is at the bottom
window.onload = function () {
  scrollToBottomOfMessages();
}
