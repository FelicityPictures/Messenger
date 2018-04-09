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

socket.on('active_user', (username, sid, all_active_users)=>{
  active_users[username]=sid;
  for (var key in all_active_users) {
    if (all_active_users[key] != undefined){
      active_users[key] = all_active_users[key];
    }
    $('#'+key).replaceWith("<h3 id='"+key+"'>" + key + " is active now</h3>");
    var p_id = "'"+"last_active_" + username + "'";
    $('#last_active_'+username).replaceWith("<p id=" + p_id + "> </p>");
  }
  if(selfUsername===username){
    $('#messages').append('<p class="chatAnnouncement">You have joined the room</p>');
  }else{
    $('#messages').append('<p class="chatAnnouncement">'+username+' joined the room</p>');
  }
  scrollToBottomOfMessages();
  console.log('active_id: '+ username);
  console.log(active_users);
});

socket.on('disconnect', function(){
  console.log('disconnected!');
});

socket.on('deactive_user', (username)=>{
  delete active_users[username];
  $('#'+username).each(function(x){
    var new_text = $(this).text().replace("is active now", "");
    $(this).text(new_text);
  })
  var dt = new Date();
  var time = dt.getFullYear() + "-0" + dt.getMonth() + "-0" + dt.getDay() + "<br>" +
  dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
  var p_id = "'"+"last_active_" + username + "'";
  $('#last_active_'+username).replaceWith("<p id=" + p_id + "> Last Active: " + time +"</p>");
  if(selfUsername===username){
    $('#messages').append('<p class="chatAnnouncement">You left the room.</p>');
  }else{
    $('#messages').append('<p class="chatAnnouncement">'+username+' has left the room.</p>');
  }
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
socket.on('new_message', (data, chat_id, username, display) => {
  if(selfUsername===username){
    $('#messages').append('<li class="self messages">'+String(data)+'</li>');
  }else{
    $('#messages').append('<li class="other messages">'+String(data)+'</li><p class="chatMessageUsername">'+username+'</p>');
  }
  scrollToBottomOfMessages();
  console.log("message sent from " + username + " to " + String(chat_id) + "!");
});

// logout button
$('#logout').click(function(){
  window.location.href = '../logout';
});

// compose button
$('#compose').click(function(){
  window.location.href = '../new_chat';
});

$('#newChatSubmit').click(function(){
  socket.emit('start_chat')
});

var lastClicked = $('#selectExistingConvos');
var currentWindow = $('#chats');
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

window.onload = function () {
  scrollToBottomOfMessages();
  $('#activeUsers').hide();
  $('#newChatBox').hide();
}
