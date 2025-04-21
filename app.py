from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    title = request.form['title']
    filename = secure_filename(file.filename)
    unique_name = str(uuid.uuid4()) + "_" + filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
    post_id = str(uuid.uuid4())
    posts.append({'id': post_id, 'title': title, 'filename': unique_name})
    return redirect('/')

@app.route('/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    return jsonify({'status': 'success'})

@app.route('/edit_title/<post_id>', methods=['POST'])
def edit_title(post_id):
    new_title = request.form['title']
    for p in posts:
        if p['id'] == post_id:
            p['title'] = new_title
            break
    return jsonify({'status': 'success'})

@app.route('/get_posts')
def get_posts():
    return jsonify(posts)

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(debug=True)
