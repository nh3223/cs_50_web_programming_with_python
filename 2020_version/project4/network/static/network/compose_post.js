function compose_post(post) {
    document.querySelector('#compose_view').style.display = 'block';
    document.querySelector('#compose_view').appendChild(get_post_form(post))
}

function get_post_form(post=null) {
    content_box = create_content_box(post)
    post_button = create_post_button(post)
    form_elements = [content_box, post_button]
    post_form = create_post_form(form_elements)
    return post_form
}

function create_content_box(post) {
    content_box = document.createElement('textarea')
    content_box.id = 'post_content'
    if (post) {
        content_box.innerHTML = `${post['content']}`
    } else {
        content_box.placeholder = 'Enter Post'
    }
    return content_box
}

function create_post_button(post) {
    const button_text = (post) ? 'Edit Post':'Make New Post';
    post_button = document.createElement('input')
    post_button.type = 'Submit'
    post_button.id = 'compose_button'
    post_button.value = button_text
    if (post) {
        post_button.addEventListener('click', () => edit_post(post))
    } else {
        post_button.addEventListener('click', () => make_post())
    }
    return post_button
}

function create_post_form(form_elements) {
   post_form = document.createElement('form')
   form_elements.forEach( function(element) {
       post_form.appendChild(element)
   })
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

function edit_post(post) {
    fetch(`/posts/${post['id']}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: document.querySelector('#post_content').value
        })
    })
    .then(response => response.json())
    .then(get_posts('all_posts'));
}