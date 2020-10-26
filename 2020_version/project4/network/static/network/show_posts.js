function get_posts(post_view_name, user_name=null) {

    clear_post_view()
    const current_user = JSON.parse(document.getElementById('current_user').textContent)
    show_post_header(post_view_name, user_name, current_user)
    if (user_name) {
        show_followers(user_name, current_user)
        post_view_name = user_name
    }
    show_posts(post_view_name, current_user)

}

function get_post_view_element() {
    return document.querySelector('#post_view')
}

function clear_post_view() {
    document.querySelector('#compose_view').style.display='none'  
    get_post_view_element().innerHTML = ''
}

function show_post_header(post_view_name, user, current_user) {
    const header_name = {'all_posts': 'All Posts', 'following': 'Following', 'profile': `${user}`, 'current_user': current_user}
    post_view_header = document.createElement('h3')
    post_view_header_text = document.createTextNode(header_name[post_view_name])
    post_view_header.appendChild(post_view_header_text)
    get_post_view_element().appendChild(post_view_header)
}

function show_followers(user_name, current_user) {

    fetch(`/posts/follows/${user_name}`)
    .then(response => response.json())
    .then(follows => {
        const follow_details = format_follows(follows, user_name, current_user)
        get_post_view_element().appendChild(follow_details)
    })
}

function format_follows(follows, user_name, current_user) {
    follow_element = document.createElement('div')
    follow_element.appendChild(get_followers_and_following(follows))
    if (user_name != current_user) {
        follow_element.appendChild(get_follow_button(follows['following'], user_name))
    }
    return follow_element
}

function get_followers_and_following(follows) {
    followers_and_following = document.createElement('h4')
    follow_text = document.createTextNode(`Followers: ${follows['number_followers']} Following: ${follows['number_following']}`)
    followers_and_following.appendChild(follow_text)
    return followers_and_following
}

function get_follow_button(following, user_name) {
    console.log('following',following)
    follow_button = document.createElement('button')
    button_text = (following) ? 'Unfollow':'Follow'
    follow_button.innerHTML = button_text
    follow_button.addEventListener('click', () => follow(following, user_name))
    return follow_button
}

function follow(following, user_name) {

    fetch(`/posts/follow/${user_name}`, {
        method: 'PUT',
        body: JSON.stringify({
            'following': !following
        })
    })
    .then(response => response.json())
    .then(get_posts('profile', user_name))
}

function show_posts(post_view_name, current_user) {

    fetch(`/posts/${post_view_name}`)
    .then(response => response.json())
    .then(posts => {
      const all_posts = format_posts(posts, current_user)
      get_post_view_element().appendChild(all_posts)
    })

}

function format_posts(posts, current_user) {
    let all_posts = document.createElement('table')
    posts.forEach(post => {
        post_details = document.createElement('tr')
        author_cell = create_author_cell(post)
        content_cell = create_content_cell(post)
        time_cell = create_time_cell(post)
        edit_cell = create_edit_cell(post, current_user)
        row_cells = [author_cell, content_cell, time_cell, edit_cell]
        post_details = get_post_details(row_cells)
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