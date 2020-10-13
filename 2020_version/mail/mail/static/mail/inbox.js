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
  document.querySelector('#read-email-view').style.display = 'none';
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
  document.querySelector('#read-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Retrieve and show emails
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
    let email_details = format_inbox(emails)
    console.log(email_details)
    document.querySelector('#emails-view').innerHTML += email_details
  });
}

function load_email(email_id) {
  
  // Show the selected email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Retrieve and show the selected email
  fetch('/emails/' + email_id)
  .then(response => response.json())
  .then(email => {
    let email_content = format_email_content(email)
    document.querySelector('#read-email-view').innerHTML = email_content
  });

  // Mark email as read
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function format_inbox(emails) {
  let email_details = ''
  emails.forEach(email => {
    email_details += `<div class="email-detail" onclick="load_email(${email['id']})" style="cursor:pointer;` 
    if (email['read'] == true) {
      console.log('TRUE')
      email_details += 'background-color: gray;'
    }
    email_details += '">'
    email_details += `From: ${email['sender']}<span class="tab">`
    email_details += `Subject: ${email['subject']}</span><span class="tab">`
    email_details += `Time: ${email['timestamp']}</span></div>`
  });
  return email_details;
}

function format_email_content(email) {
  // Show general email content
  let email_content = '<div>'
  email_content += `From: ${email['sender']}<hr>`
  email_content += `To: ${email['recipients']}<hr>`
  email_content += `Time: ${email['timestamp']}<hr>`
  email_content += `Subject: ${email['subject']}<hr>`
  email_content += `Body: ${email['body']}</div>`

  // Add archive button
  let button_value = 'Archive'
  if (email['archived'] == true) {
    button_value = 'Remove from Archive'
  }
  email_content += `<button class="btn btn-sm btn-outline-primary" id="archive">${button_value}</button>`
  return email_content
}