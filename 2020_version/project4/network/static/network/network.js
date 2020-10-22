document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#all_posts').addEventListener('click', () => get_posts('all_posts'));
    document.querySelector('#following').addEventListener('click', () => get_posts('following'));
    document.querySelector('#current_user').addEventListener('click', () => get_posts('current_user'));
    document.querySelector('#new_post').addEventListener('click', () => compose_post(null));
    
    get_posts('all_posts');
  });

  function compose_post(post) {

    // Display Compose Window
    document.querySelector('#compose_view').style.display = 'block';

    // Display Form
    document.querySelector('#compose_view').appendChild(get_post_form(post))

}

function get_posts(posts, user=null) {

    // Hide New/Edit Post Form and Clear Posts View
    document.querySelector('#compose_view').style.display='none'  
    post_view = document.querySelector('#post_view')
    post_view.innerHTML = ''

    // Identify Profile Posts
    current_user = document.getElementById('current_user').innerHTML.slice(8,-9)
    if (posts == 'current_user') {
        profile_name = current_user
        posts = 'profile'
    } else if (posts == 'profile') {
        profile_name = user
    } else {
        profile_name = posts
    }

    // Show the Posts View Name
    post_view_names = {'all_posts': 'All Posts', 'following': 'Following', 'profile': profile_name}
    post_view_header = document.createElement('h3')
    post_view_header_text = document.createTextNode(`${post_view_names[posts]}`)
    post_view_header.appendChild(post_view_header_text)
    post_view.appendChild(post_view_header)

    // Retrieve and show posts

    fetch(`/posts/${profile_name}`)
    .then(response => response.json())
    .then(posts => {
      let all_posts = format_posts(posts, current_user, profile_name)
      post_view.appendChild(all_posts)
    })

}

function get_post_form(post=null) {
    let button_text = (post) ? 'Edit Post':'Make New Post';
    let placeholder = (post) ? post['content']:'Enter Post'
    post_form = document.createElement('form')
    // Set up content area
    content_area = document.createElement('textarea')
    content_area.id = 'post_content'
    content_area.placeholder = placeholder
    // Set up break
    break_line = document.createElement('br')
    // Set up submit button
    submit_button = document.createElement('input')
    submit_button.type = 'Submit'
    submit_button.id = 'compose_button'
    submit_button.value = button_text
    submit_button.addEventListener('click', () => make_post(post))
    // Put the Form Together
    post_form.appendChild(content_area)
    post_form.appendChild(break_line)
    post_form.appendChild(submit_button)



    //post_form = '<form>'
    //post_form += `<textarea id="post_content" placeholder=${placeholder}></textarea><br>`
    //post_form += `<input type="Submit" id="compose_button" value=${button_text} onclick="make_post(${post})">`;
    //post_form += '</form>'
    return post_form
}

function make_post() {

    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
          content: document.querySelector('#post_content').value
        })
      })
      .then(response => response.json())
      .then(get_posts('all_posts'));
}

function format_posts(posts, current_user, profile_name) {
    // Create Posts Table
    let all_posts = document.createElement('table')
    posts.forEach(post => {
        // Create Post Row
        post_details = document.createElement('tr')
        // Create Author Cell
        author_cell = document.createElement('td')
        author_cell.classList.add('post_author')
        author_cell.addEventListener('click', () => get_posts('profile',post['author']))
        author_text = document.createTextNode(`${post['author']}`)
        author_cell.appendChild(author_text)
        // Create Content Cell
        content_cell = document.createElement('td')
        content_text = document.createTextNode(`${post['content']}`)
        content_cell.appendChild(content_text)
        // Create Time Cell
        time_cell = document.createElement('td')
        time_text = document.createTextNode(`${post['timestamp']}`)
        time_cell.appendChild(time_text)
        // Create Edit Button Cell
        edit_cell = document.createElement('td')
        edit_button = document.createElement('button')
        edit_button.classList.add('edit_button')
        edit_button.innerHTML = 'Edit'
        edit_button.addEventListener('click', () => compose_post(post))
        edit_cell.appendChild(edit_button)
        // Combine Entire Row
        post_details.appendChild(author_cell)
        post_details.appendChild(content_cell)
        post_details.appendChild(time_cell)
        if (current_user == post['author']) {
            post_details.appendChild(edit_cell)
        }
        // Add Row to Table
        all_posts.appendChild(post_details)
    })
      //post_details += `<div class="profile" onclick="get_posts('profile','${post['author']}')" style="cursor:pointer;">Author: ${post['author']}<span class="tab">`
      //post_details += `<span class="tab">Content: ${post['content']}</span>`
      //post_details += `<span class="tab">Time: ${post['timestamp']}</span>`
      //if (current_user == post['author']) {
      //     post_id = `post_${post['id']}`
      //      post_details += '<span class="tab"><button class="edit_post">Edit</button></span>'//
      //console.log(post_details)
      //}
    //});
    //return post_details;
    return all_posts
}