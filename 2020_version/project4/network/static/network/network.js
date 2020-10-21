document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#all_posts').addEventListener('click', () => get_posts('all_posts'));
    document.querySelector('#following').addEventListener('click', () => get_posts('following'));
    document.querySelector('#current_user').addEventListener('click', () => get_posts('current_user'));
    document.querySelector('#new_post').addEventListener('click', () => compose_post(null));
    //document.querySelector('#edit_post').addEventListener('click', () => compose_post(post));  
  
    // By default, load all posts
    get_posts('all_posts');
  });

  function compose_post(post) {
    console.log('Enter compose_post_function')  
    // Display Compose Window
    document.querySelector('#compose_view').style.display = 'block';

    // Display Form
    document.querySelector('#compose_view').innerHTML = get_post_form(post)

}

function get_posts(posts, user=null) {

    // Hide New/Edit Post Form
    document.querySelector('#compose_view').style.display='none'  
    
    // Identify Profile Posts
    if (posts == 'current_user') {
        profile_name = document.getElementById('current_user').innerHTML.slice(8,-9)
        posts = 'profile'
    } else if (posts == 'profile') {
        profile_name = user
    } else {
        profile_name = posts
    }

    // Show the Posts View Name
    post_view_names = {'all_posts': 'All Posts', 'following': 'Following', 'profile': profile_name}
    document.querySelector('#post_view').innerHTML = `<h3>${post_view_names[posts]}</h3>`;
  
    // Retrieve and show emails
    
    path = `/posts/${posts}`
    if (profile_name != '') {
        path += `/${profile_name}`
    }

    fetch(`/posts/${profile_name}`)
    .then(response => response.json())
    .then(posts => {
      console.log(posts)
      let post_details = format_posts(posts)
      document.querySelector('#post_view').innerHTML += post_details
    });

}

function get_post_form(post=null) {
    let button_text = (post) ? 'Edit Post':'Make New Post';
    console.log(button_text)
    let placeholder = (post) ? post['content']:'Enter Post'
    post_form = '<form>'
    post_form += `<textarea id="post_content" placeholder=${placeholder}></textarea><br>`
    post_form += `<input type="Submit" id="compose_button" value=${button_text} onclick="make_post(${post})">`;
    post_form += '</form>'
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

function format_posts(posts) {
    let post_details = ''
    posts.forEach(post => {
      post_details += `<div class="profile" onclick="get_posts('profile','${post['author']}')" style="cursor:pointer;">Author: ${post['author']}</div><span class="tab">`
      post_details += `Content: ${post['content']}</span><span class="tab">`
      post_details += `Time: ${post['timestamp']}</span>`
    });
    return post_details;
}