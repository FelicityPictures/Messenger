var active_users = {};

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
});

socket.on('active_user', (username, sid)=>{
  active_users[username]=sid;
  $('#messages').append('<p class="chatAnnouncement">'+username+' joined the room</p>')
  scrollToBottomOfMessages();
  console.log('active_id: '+ username);
  console.log(active_users);
});

socket.on('disconnect', function(){
  console.log('disconnected!');
});

socket.on('deactive_user', (username)=>{
  delete active_users[username]
  $('#messages').append('<p class="chatAnnouncement">'+username+' has left the room.</p>');
  scrollToBottomOfMessages();
  console.log('deactive_user: '+ username);
  console.log(active_users);
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
socket.on('new_message', (data, chat_id, username) => {
  console.log("heres");
  $('#messages').append('<li>'+String(data)+'</li><p class="chatMessage">'+username+'</p>');
  scrollToBottomOfMessages();
  console.log("message sent from " + username + " to " + String(chat_id) + "!");
});

// logout button
$('#logout').click(function(){
  window.location.href = '../logout';
});

// compose button
$('#compose').click(function(){
  // $('#chatBox').hide();
  // $('#newChatBox').show();
  window.location.href = '../new_chat';
});

$('#newChatSubmit').click(function(){
  socket.emit('start_chat')
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
