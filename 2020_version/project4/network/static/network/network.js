document.addEventListener('DOMContentLoaded', function() {

    current_user = JSON.parse(document.getElementById('current_user').textContent)
    // Use buttons to toggle between views
    document.querySelector('#all_posts').addEventListener('click', () => get_posts('all_posts'));
    document.querySelector('#following').addEventListener('click', () => get_posts('following'));
    document.querySelector('#current_user_element').addEventListener('click', () => get_posts('profile', current_user));
    document.querySelector('#new_post').addEventListener('click', () => compose_post(null));
    
    get_posts('all_posts');
  });