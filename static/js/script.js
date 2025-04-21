function loadPosts() {
  fetch('/get_posts')
    .then(res => res.json())
    .then(data => {
      const postsDiv = document.getElementById('posts');
      postsDiv.innerHTML = '';
      data.forEach(post => {
        const postElem = document.createElement('div');
        postElem.className = 'post';
        postElem.innerHTML = `
          <strong>Title:</strong> <span contenteditable="true" onblur="editTitle('${post.id}', this.innerText)">${post.title}</span>
          <img src="/static/uploads/${post.filename}">
          <button onclick="deletePost('${post.id}')">Delete</button>
        `;
        postsDiv.appendChild(postElem);
      });
    });
}

function deletePost(id) {
  fetch(`/delete/${id}`, { method: 'POST' })
    .then(res => res.json())
    .then(() => loadPosts());
}

function editTitle(id, newTitle) {
  fetch(`/edit_title/${id}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `title=${encodeURIComponent(newTitle)}`
  }).then(() => loadPosts());
}

setInterval(loadPosts, 2000); // Real-time refresh every 2 seconds
window.onload = loadPosts;
