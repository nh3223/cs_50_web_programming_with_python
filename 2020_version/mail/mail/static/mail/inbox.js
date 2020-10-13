document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  //.then(response => response.json())
  .then(response => {
    console.log(response)
  })
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Retrieve and show emails
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      let email_details = '<div class="email-detail '
      if (email['read'] == true) {
        email_details += 'style="background-color: gray '
      }
      email_details += `>From: ${email['sender']}<span class="tab">`
      email_details += `Subject: ${email['subject']}</span><span class="tab">`
      email_details += `Time: ${email['timestamp']}</span></div>`
      document.querySelector('#emails-view').innerHTML += email_details
    })
  });
   

  //document.querySelector('#emails-view').append(element);
}