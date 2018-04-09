$("#newChatForm").submit((e) => {
  e.preventDefault();
  emit_to_users_in_chat();
})

function emit_to_users_in_chat(){
  console.log('Tell everyone to join room');
  formInfo = $('newChatForm').serialize();
  console.log(formInfo);
}
