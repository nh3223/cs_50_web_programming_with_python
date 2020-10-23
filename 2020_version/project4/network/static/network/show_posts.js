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
      let all_posts = format_posts(posts, current_user)
      post_view.appendChild(all_posts)
    })

}

function format_posts(posts, current_user) {
    // Create Posts Table
    let all_posts = document.createElement('table')
    posts.forEach(post => {
        // Create Post Row
        post_details = document.createElement('tr')
        // Create Cells
        author_cell = create_author_cell(post)
        content_cell = create_content_cell(post)
        time_cell = create_time_cell(post)
        edit_cell = create_edit_cell(post, current_user)
        // Create Row
        row_cells = [author_cell, content_cell, time_cell, edit_cell]
        post_details = get_post_details(row_cells)
        // Add row to table
        all_posts.appendChild(post_details)
    })

    return all_posts
}

function create_author_cell(post) {
    author_cell = document.createElement('td')
    author_cell.classList.add('post_author')
    author_cell.addEventListener('click', () => get_posts('profile',post['author']))
    author_text = document.createTextNode(`${post['author']}`)
    author_cell.appendChild(author_text)
    return author_cell
}

function create_content_cell(post) {
    content_cell = document.createElement('td')
    content_text = document.createTextNode(`${post['content']}`)
    content_cell.appendChild(content_text)
    return content_cell
}

function create_time_cell(post) {
    time_cell = document.createElement('td')
    time_text = document.createTextNode(`${post['timestamp']}`)
    time_cell.appendChild(time_text)
    return time_cell
}

function create_edit_cell(post, current_user) {
    edit_cell = document.createElement('td')
    if (current_user != post['author']) {
        return edit_cell
    }
    edit_button = document.createElement('button')
    edit_button.classList.add('edit_button')
    edit_button.innerHTML = 'Edit'
    edit_button.addEventListener('click', () => compose_post(post))
    edit_cell.appendChild(edit_button)
    return edit_cell
}

function get_post_details(row_cells) {
    post_details = document.createElement('tr')
    row_cells.forEach( function(cell) {
        post_details.appendChild(cell)
    })
    return post_details
}