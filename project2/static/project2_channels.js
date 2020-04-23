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

function create_and_add_list_element(item) {
    var a = document.createElement("a");
    var text = document.createTextNode(item);
    var line_break = document.createElement("br");
    a.appendChild(text);
    a.title = text
    a.href = text;
    document.getElementById("channel_list").appendChild(a);
    document.getElementById("channel_list").appendChild(line_break);
};

function list_channel_names(channel_names) {
    var channel_list = document.getElementById("channel_list");
    channel_names.forEach(function(item) {
        create_and_add_list_element(item);
    });
}

document.querySelector('#new_channel_form').onsubmit = () => {
    const request = new XMLHttpRequest();
    const new_channel_name = document.querySelector('#new_channel_name').value;
    if (new_channel_name in channels) {
        alert('That channel already exists.');
        return false;
    } else {
        request.open('POST', '/create_channel');
        request.onload = () => {
            const data = JSON.parse(request.responseText)
            alert(data.success);
            if (data.success) {
                create_and_add_list_element(new_channel_name);
            } else {
                alert('There was a problem');
            };
        };
        const data = new FormData();
        data.append('new_channel_name', new_channel_name);
        request.send(data);
        return false;
    };
};




var channel_names = Object.keys(channels)
list_channel_names(channel_names)



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