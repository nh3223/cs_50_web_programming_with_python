function get_posts(post_view_name, user_name=null) {
    
    const current_user = JSON.parse(document.getElementById('current_user').textContent)
    document.getElementById('compose_view').style.display='none'
    show_post_header(post_view_name, user_name, current_user)
    if (user_name) {
        show_followers(user_name, current_user)
        post_view_name = user_name
    } else {
        document.getElementById('follow_table').style.display='none'
    }
    show_posts(post_view_name, current_user)
}

function show_post_header(post_view_name, user, current_user) {
    const header_name = {'all_posts': 'All Posts', 'following': 'Following', 'profile': `${user}`, 'current_user': current_user}
    post_view_header = document.getElementById('post_header')
    post_view_header.innerHTML = header_name[post_view_name]
}

function show_followers(user_name, current_user) {

    fetch(`/posts/follows/${user_name}`)
    .then(response => response.json())
    .then(follows => {
        format_follows(follows, user_name, current_user)
    })
}

function format_follows(follows, user_name, current_user) {
    document.getElementById('follow_table').innerHTML = ''
    add_followers_and_following(follows)
    if (user_name != current_user) {
        add_follow_button(follows['following'], user_name)
    }
}

function add_followers_and_following(follows) {
    followers_row = document.createElement('tr')
    followers = document.createElement('td')
    followers.innerHTML = `Followers: ${follows.number_followers}`
    following = document.createElement('td')
    following.innerHTML = `Following: ${follows.number_following}`
    followers_row.appendChild(followers)
    followers_row.appendChild(following)
    document.getElementById('follow_table').appendChild(followers_row)
}

function add_follow_button(following, user_name) {
    follow_button_cell = document.createElement('td')
    follow_button = document.createElement('button')
    button_text = (following) ? 'Unfollow':'Follow'
    follow_button.innerHTML = button_text
    follow_button.addEventListener('click', () => follow(following, user_name))
    follow_button_cell.appendChild(follow_button)
    document.getElementById('follow_table').appendChild(follow_button_cell)
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

function show_posts(post_view_name, current_user, page=1) {
    console.log('show_posts', page)
    fetch(`/posts/${post_view_name}/${page}`)
    .then(response => response.json())
    .then(posts => {
        format_posts(posts.posts, current_user)
        console.log(posts.page)
        show_pagination(post_view_name, current_user, posts.page, posts.last_page)
    })
}

function format_posts(posts, current_user) {
    document.getElementById('post_table').innerHTML = ''
    posts.forEach(post => {
        create_and_populate_row(post, current_user)
    })
}

async function create_and_populate_row(post, current_user) {
    all_posts = await document.getElementById('post_table')
    const cell_names = ['author', 'content', 'time', 'like', 'like_button', 'edit']
    await create_post_row(post.id, cell_names)
    add_post_content(post, current_user)
} 

function create_post_row(post_id, cell_names) {
    // Create cells
    all_posts = document.getElementById('post_table')
    let row = document.createElement('tr')
    cell_names.forEach(name => {
        let cell = document.createElement('td')
        cell.id = `${name}_${post_id}`
        cell.classList.add(`${name}`)
        row.appendChild(cell)
    all_posts.appendChild(row)
    })
}

function add_post_content(post, current_user) {
    add_author_content(post)
    add_content_content(post)
    add_time_content(post)
    add_like_content(post)
    add_like_button_content(post, current_user)
    add_edit_content(post, current_user)
}

function add_author_content(post) {
    author_cell = document.getElementById(`author_${post.id}`)
    author_cell.addEventListener('click', () => get_posts('profile', post['author']))
    author_text = document.createTextNode(`${post['author']}`)
    author_cell.appendChild(author_text)
}

function add_content_content(post) {
    content_cell = document.getElementById(`content_${post.id}`)
    content_text = document.createTextNode(`${post['content']}`)
    content_cell.appendChild(content_text)
}

function add_time_content(post) {
    time_cell = document.getElementById(`time_${post.id}`)
    time_text = document.createTextNode(`${post['timestamp']}`)
    time_cell.appendChild(time_text)
}

function add_edit_content(post, current_user) {
    edit_cell = document.getElementById(`edit_${post.id}`)
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

function add_like_content(post) {    
    like_cell = document.getElementById(`like_${post.id}`)
    like_cell.innerHTML = ''
    like_cell_text = document.createTextNode(`Likes: ${post.likes.length}`)
    like_cell.appendChild(like_cell_text)
}
    
function add_like_button_content(post, current_user) {
    let like_cell = document.getElementById(`like_button_${post.id}`)
    like_cell.innerHTML = ''
    let user_likes = post.likes.includes(current_user)
    if (current_user !=post.author) {
        let like_button = document.createElement('button')
        like_button.id = `like_button_button_${post.id}`
        like_button.innerHTML = (user_likes) ? 'Unlike':'Like'
        like_button.addEventListener('click', () => like(post, current_user))
    like_cell.appendChild(like_button)
    }
}

function like(post, current_user) {

    liked = post.likes.includes(current_user)
    fetch(`/posts/like/${post.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            'liked': liked
        })
    })
    .then(response => response.json())
    .then(post => {
        add_like_content(post)
        add_like_button_content(post)
    })
}

function show_pagination(post_view_name, current_user, page, last_page) {
    console.log('show_pagination', page, last_page)
    document.getElementById('pagination').innerHTML = ''
    if (page != 1) {
        create_page_button(post_view_name, current_user, 'Previous', page)
    }
    document.getElementById('pagination').appendChild(document.createTextNode(`Page ${page}`))
    if (page != last_page) {
        create_page_button(post_view_name, current_user, 'Next', page)
    }
}

function create_page_button(post_view_name, current_user, button_type, page) {
    console.log('create_page_button', page)
    let page_button = document.createElement('button')
    page_button.innerHTML = button_type
    if (button_type == 'Previous') {
        page_button.addEventListener('click', () => show_posts(post_view_name, current_user, page - 1))
    } else {
        page_button.addEventListener('click', () => show_posts(post_view_name, current_user, page + 1))
    }
    document.getElementById('pagination').appendChild(page_button)
}