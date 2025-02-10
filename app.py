from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Sample blog posts
test_posts = [
    {"id": 1, "title": "First Post", "excerpt": "This is the first blog post.", "content": "Full content of first post.", "category": "General", "date": "2025-01-15"},
    {"id": 2, "title": "Tech News", "excerpt": "Latest in technology.", "content": "Full content of tech news.", "category": "Technology", "date": "2025-02-01"},
]

@app.route('/')
def index():
    return render_template('index.html', posts=test_posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = next((p for p in test_posts if p["id"] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    return "Post not found", 404

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        new_post = {
            "id": len(test_posts) + 1,
            "title": request.form['title'],
            "excerpt": request.form['content'][:50] + "...",
            "content": request.form['content'],
            "category": request.form['category'],
            "date": datetime.today().strftime('%Y-%m-%d')
        }
        test_posts.append(new_post)
        return redirect(url_for('index'))
    return render_template('add_post.html')

@app.route('/category')
def filter_by_category():
    category = request.args.get('category')
    filtered_posts = [p for p in test_posts if p['category'] == category] if category else test_posts
    return render_template('index.html', posts=filtered_posts)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = next((p for p in test_posts if p["id"] == post_id), None)
    if not post:
        return "Post not found", 404
    
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        post['category'] = request.form['category']
        post['excerpt'] = request.form['content'][:50] + "..."
        return redirect(url_for('index'))
    
    return render_template('edit_post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
