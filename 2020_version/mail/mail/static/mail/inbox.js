document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(null));
  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if (email === null) {
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {
    // Populate Fields on Reply
    document.querySelector('#compose-recipients').value = `${email['sender']}`
    document.querySelector('#compose-subject').value =  `Re: ${email['subject']}`
    document.querySelector('#compose-body').value = `On ${email['timestamp']}, ${email['sender']} wrote: \n${email['body']}`
  }
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
    document.querySelector('#archive').addEventListener('click', () => archive_email(email))
    document.querySelector('#reply').addEventListener('click', () => compose_email(email));
  });

  // Mark email as read
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function archive_email(email) {
  if (email['archived'] === true) {
    archive_value = false
  } else {
    archive_value = true
  }
  fetch('/emails/' + email['id'], {
    method: 'PUT',
    body: JSON.stringify({
      archived: archive_value
    })
  })
  .then(load_mailbox('inbox'));
}

function format_inbox(emails) {
  let email_details = ''
  emails.forEach(email => {
    email_details += `<div class="email-detail" onclick="load_email(${email['id']})" style="cursor:pointer;` 
    if (email['read'] == true) {
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
  email_content += `Body: ${email['body']}</div><hr>`

  // Add archive button
  let button_value = 'Archive'
  if (email['archived'] == true) {
    button_value = 'Remove from Archive'
  }
  email_content += `<button class="btn btn-sm btn-outline-primary" id="archive">${button_value}</button>`
  
  // Add reply button
  email_content += '<button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>'
  return email_content
}