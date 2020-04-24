function create_and_add_list_element(item) {
    var a = document.createElement("a");
    var text = document.createTextNode(item);
    var line_break = document.createElement("br");
    a.appendChild(text);
    a.title = text;
    a.href = '#';
    a.onclick = function() {
        load_messages(item);
    };
    document.getElementById("channel_list").appendChild(a);
    document.getElementById("channel_list").appendChild(line_break);
};

function list_channel_names(channel_names) {
    var channel_list = document.getElementById("channel_list");
    channel_names.forEach(function(item) {
        create_and_add_list_element(item);
    });
};

function create_new_channel (request, new_channel_name) {
    request.open('POST', '/create_channel');
    request.onload = () => {
        const data = JSON.parse(request.responseText)
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
}

document.querySelector('#new_channel_form').onsubmit = () => {
    const request = new XMLHttpRequest();
    const new_channel_name = document.querySelector('#new_channel_name').value;
    document.querySelector('#new_channel_name').value = '';
    if (new_channel_name in channels) {
        alert('That channel already exists.');
        return false;
    } else {
        create_new_channel(request, new_channel_name)
    };
};

var channel_names = Object.keys(channels)
list_channel_names(channel_names)



