function generate_messages(table, messages) {
    for (let message of messages) {
        generate_row(table, message)
    };
};

function generate_row(table, message) {
    let row = table.insertRow(0);
    row.insertCell().appendChild(document.createTextNode(message['display_name']))
    row.insertCell().appendChild(document.createTextNode(message['text']))
    row.insertCell().appendChild(document.createTextNode(message['timestamp']))
};

function load_messages(channel) {
    localStorage.setItem('channel', channel)
    document.querySelector('#show_messages').style.visibility = "visible";
    document.querySelector('#channel_name').innerHTML = channel;
    let table = document.querySelector('#message_list');
    table.innerHTML = ""
    let messages = channels[channel];
    generate_messages(table, messages);
};

var socket = io.connect();

socket.on('connect', () => {
    document.querySelector('#message_form').onsubmit = () => {
        let message_text = document.querySelector('#message_text').value;
        document.querySelector('#message_text').value = "";
        let user_name = localStorage.getItem('user_name');
        let channel_name = document.querySelector('#channel_name').innerHTML
        let message_data = { 'channel_name': channel_name, 'message_text': message_text, 'user_name': user_name }
        socket.emit('submit message', message_data);
        return false;
    };
});

socket.on('new message', data => {
    let table = document.querySelector('#message_list');
    generate_row(table,data);
    return false;
});


if (localStorage.getItem('channel')) {
    load_messages(localStorage.getItem('channel'));
} else {
    document.querySelector('#show_messages').style.visibility = "hidden";
};
