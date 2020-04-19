function welcome(user_name) {

    /* This function performs the following actions:
            (1) Hides the form for entering a display name
            (2) Prints a greeting
            (3) Shows a button to click if the display name is not the current user
            (4) Upon clicking the button, hides the greeting and button, and calls the get_user_name function*/

    document.querySelector('#display_name_form').style.visibility="hidden";
    document.querySelector('#Greeting').innerHTML = 'Hello, ' + user_name;
    document.querySelector('#not_name').innerHTML = 'Not ' + user_name + '?';
    document.querySelector('#not_name').onclick = () => {
        document.querySelector('#Greeting').style.visibility="hidden";
        document.querySelector('#not_name').style.visibility="hidden";
        get_user_name();
    }
}

function get_user_name() {
    
    /* This function performs the following functions:
            (1) Shows the form for entering a display name
            (2) On submission of display name, sets the local starage user_name and calls the welcome function. */
    
    document.querySelector('#display_name_form').style.visibility="visible";
    document.querySelector('#display_name_form').onsubmit = () => {
        localStorage.setItem('user_name', document.querySelector('#display_name').value);
        welcome(localStorage.getItem('user_name'))
    }
}

// If a user_name is saved in localStorage, calls the welcome function, otherwise calls the get_user_name function.

if(localStorage.getItem('user_name')) {
    welcome(localStorage.getItem('user_name'));   
} else {
    get_user_name();
}
