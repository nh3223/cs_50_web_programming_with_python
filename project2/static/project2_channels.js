function generate_messages(table, messages) {
    for (let message of messages) {
        generate_row(table,message)
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

var channel_name = channel_data['channel_name'];
var messages = channel_data['messages'];

document.querySelector('h1').innerHTML = channel_name;

let table = document.querySelector('table');
generate_messages(table, messages)


var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

socket.on('connect', () => {
    document.querySelector('#message_form').onsubmit = () => {
        alert(he)
        let message_text = document.querySelector('#message_text').value;
        let user_name = localStorage.getItem('user_name');
        let message_data = { 'channel_name': channel_name, 'message_text': message_text, 'user_name': user_name }
        alert(message_data)
        socket.emit('submit message', message_data);
    };
});

socket.on('new_message', data => {
    
    generate_row(table,data);
});