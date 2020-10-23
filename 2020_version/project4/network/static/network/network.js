document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#all_posts').addEventListener('click', () => get_posts('all_posts'));
    document.querySelector('#following').addEventListener('click', () => get_posts('following'));
    document.querySelector('#current_user').addEventListener('click', () => get_posts('current_user'));
    document.querySelector('#new_post').addEventListener('click', () => compose_post(null));
    
    get_posts('all_posts');
  });