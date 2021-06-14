document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = () => { send() };
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

   fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
    // Print emails
    emails.forEach((email) => {

        let element = document.createElement('div');

        if (email.read == true && mailbox == 'inbox') {
            element.innerHTML = `<table class="div5"><tbody><tr><td class="div2">From: ${email.sender}</td>
            <td class="div3">${email.subject}</td> <td class="div4">${email.timestamp}</td></tr></tbody></table>`;
        } else {
            element.innerHTML = `<table class="div1"><tbody><tr><td class="div2">From: ${email.sender}</td>
            <td class="div3">${email.subject}</td> <td class="div4">${email.timestamp}</td></tr></tbody></table>`;
        }

        if (mailbox == 'sent') {
            element.innerHTML = `<table class="div1"><tbody><tr><td class="div2">To: ${email.recipients}</td>
            <td class="div3">${email.subject}</td> <td class="div4">${email.timestamp}</td></tr></tbody></table>`;
        }

        element.addEventListener('click', function() {
 //           console.log('This element has been clicked!');
            view(email.id);
    });

        document.querySelector('#emails-view').append(element);
    });
    });
}

function send() {
    let recipients = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
        read: false
        }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.message == "Email sent successfully.") {
         load_mailbox('inbox');
    } else {
        alert(result.error);
    }
    });
}

function view(id) {

    document.querySelector('#emails-view').innerHTML = '';
    fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(email => {
        document.querySelector("#emails-view").innerHTML = "";
        let element = document.createElement('div');

        element.innerHTML = `<div class="view">
        <span class="text1">From: </span>${email.sender}<br>
        <span class="text1">To: </span>${email.recipients}<br>
        <span class="text1">Subject: </span>${email.subject}<br>
        <span class="text1">Timestamp: </span>${email.timestamp}<br>
        <hr>
        <div style="white-space: pre">${email.body}</div>
        <hr>
        </div>`;

        document.querySelector('#emails-view').append(element);

   let arch = document.createElement('span');

   if (email.archived == false) {
       arch.innerHTML = `<span class="view">
           <button class="btn btn-sm btn-outline-primary" id="archived">Archive</button>
       </span>`;
   } else {
       arch.innerHTML = `<span class="view">
           <button class="btn btn-sm btn-outline-primary" id="archived">Unarchive</button>
       </span>`;
   }

   arch.addEventListener('click', function() {
       archch(email.id, email.archived);
       view(id);
       view(id);
    });

   document.querySelector('#emails-view').append(arch);


   let reply = document.createElement('span');

    reply.innerHTML = `<span class="view">
       <button class="btn btn-sm btn-outline-primary" id="archived">Reply</button>
    </span>`;

   reply.addEventListener('click', function() {
        rep(email.sender, email.subject, email.timestamp, email.body);
    });

   document.querySelector('#emails-view').append(reply);

   read(id);
 });
}

function archch(id, archived) {

    let a;
    if (archived == true) {
        a = false;
    } else {
        a = true;
    }

    fetch(`/emails/${id}`, {
    method: 'PUT',
        body: JSON.stringify({
        archived: a
        })
    })
}

function rep(sender, subject, timestamp, body) {
    compose_email();

    document.querySelector('#compose-recipients').value = sender;
    document.querySelector('#compose-subject').value = 'Re: ' + subject;
    document.querySelector('#compose-body').value = 'On ' + timestamp + ' ' + sender + ' wrote:\n' + body + '\n\n';

    document.querySelector('#compose-form').onsubmit = () => { send() };
      document.querySelector("#compose-body").value = pre_fill;
}

function read(id) {
    fetch(`/emails/${id}`, {
    method: 'PUT',
        body: JSON.stringify({
        read: true
        })
    })
}
