function generate_messages(table, messages) {
    table.innerHTML = ""
    for (let message of messages) {
        generate_row(table, message)
    }
}
function generate_row(table, message) {
    let row = table.insertRow(0);
    for (key in message) {
        let cell = row.insertCell();
        let text = document.createTextNode(message[key]);
        cell.appendChild(text);
    }
}

function load_messages(channel) {
    document.querySelector('#show_messages').style.visibility = "visible";
    document.querySelector('#messages_title').innerHTML = `${channel} messages`;
    let table = document.querySelector('#message_list');
    let messages = channels[channel];
    generate_messages(table, messages);
    return false;
};

document.querySelector('#show_messages').style.visibility="hidden";
/*
var messages = channel_data['messages'];



let table = document.querySelector('table');
generate_messages(table, messages)


var socket = io.connect();

socket.on('connect', () => {
    document.querySelector('#message_form').onclick = () => {
        let message_text = document.querySelector('#message_text').value;
        let user_name = localStorage.getItem('user_name');
        let message_data = { 'channel_name': channel_name, 'message_text': message_text, 'user_name': user_name }
        socket.emit('submit message', message_data);
    };
});
socket.on('new_message', data => {
        generate_row(table,data);
});
*/