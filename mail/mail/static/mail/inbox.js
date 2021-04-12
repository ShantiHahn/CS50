

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // use button to send email 
  document.querySelector('form').onsubmit = send_email; 

  // By default, load the inbox
  load_mailbox('inbox');

  //add current state to the history
  
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

function reply_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = 'Re:' + email.subject;
  document.querySelector('#compose-body').value =   'On ' + email.timestamp + ' ' +email.sender + " wrote: " + email.body ;




}

//function send email ?
function send_email() {

  

  //load data into variables
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  //request post 
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json());
  load_mailbox('sent');
  console.log("email sent");
  return false;
  



}


//get email by id


function get_email_by_id(email) {
  let email_id = email.id;
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then( email => {
    let div = document.createElement("div");
    div.id = "mail";
    div.innerHTML = "Sender: " + email.sender + "<br>" + "recipients: " + email.recipients + "<br> " + "Subject: " + email.subject + "<br>" + email.timestamp + "<br>"; 
    //access the email view and mark as read
    div.addEventListener('click', () => {
  
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
      view_email(email);
    });

    //create mail container
    let mail_container = document.createElement("div");
    mail_container.id = 'mail-container';
    //create buttons container
    let btn_container = document.createElement("div");
    btn_container.id = 'btn-container';

    //create buttons for replay and archive
    let btn_reply = document.createElement("button");
    let btn_archive = document.createElement("button");
    btn_reply.id ='btn';
    btn_reply.setAttribute("class", "btn btn-sm btn-outline-primary");
    btn_archive.id = 'btn';
    btn_archive.setAttribute("class", "btn btn-sm btn-outline-primary");
    btn_reply.innerHTML = "Reply";

    if(email.archived) {
      btn_archive.innerHTML = "Unarchive";
    } else {
        btn_archive.innerHTML = "Archive";

    }

    // reply

    btn_reply.addEventListener('click', () => {
      reply_email(email);
    });
    
    // PUT fetch for archive or unarchive
    btn_archive.addEventListener('click', () => {

      if(email.archived) {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: false
          })
        });


      } else {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: true
          })
        });


      };

      //mail_container.style.animationPlayState= 'running';

      // Once the mail is archived or unarchived we load the inbox but it doesn't always refresh sadly
      load_mailbox('inbox');
      
    })

    mail_container.appendChild(div);
    mail_container.appendChild(btn_container);
    btn_container.appendChild(btn_archive);
    btn_container.appendChild(btn_reply);
    document.getElementById("box-view").appendChild(mail_container);
    if ( email.read ) {
      div.style.backgroundColor = 'lightgray' ;
    } else {
      div.style.backgroundColor = 'white' ;
    };
  });
}


//view email function
function view_email(email) {
  document.querySelector('#box-view').style.display= 'none';
  document.querySelector('#emails-view').innerHTML = `<h3> Email id ${email.id} </h3>`;
  let div = document.createElement("div");
  div.id = "mail_view";
  div.innerHTML = "Sender: " + email.sender + "<br>" + "Recipients: " + email.recipients + "<br> " + "Subject: " + email.subject + "<br>" + email.timestamp + "<br>" + email.body; 
  document.getElementById('emails-view').appendChild(div);
}
 




function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  console.log('load');
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';



  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  const inbox_view = document.createElement("div");
  inbox_view.id = "box-view";
  document.getElementById("emails-view").appendChild(inbox_view);
  // Load emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    //console.log(response)

    if(mailbox != 'archive') {
      emails.forEach(email => {
        if( !email.archived) {
          get_email_by_id(email);
        }
        
      });
    } else {
      emails.forEach(email => {
        if( email.archived) {
          get_email_by_id(email);
        }
        
      });
    }



  })


}
