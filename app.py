# post_service.py

from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

posts = {
        '1': {'user_id': '1', 'post': 'Hello, world!'},
        '2': {'user_id': '2', 'post': 'My first blog post'}
    }
@app.route("/")
def home():
    return "post service is live!"

@app.route('/post/<id>')
def post(id):
    post_info = posts.get(id, {})
    
    # Get user info from User Service
    if post_info:
        response = requests.get(f'http://user_service:5000/user/{post_info["user_id"]}')
        if response.status_code == 200:
            post_info['user'] = response.json()

    return jsonify(post_info)

@app.route('/post/<id>', methods=['GET'])
def read_post(id):
    return jsonify(posts.get(id, {}))

@app.route('/post/<id>', methods=['POST'])
def create_post():
    id=request.json.get('id')
    userId = request.json.get('user_id')
    post = request.json.get('post')
    posts[id] = {'user_id': userId, 'post': post}
    return jsonify(posts[id]), 201

@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    if id in posts:
        userId = request.json.get('user_id')
        post = request.json.get('post')
        posts[id] = {'user_id': userId, 'post': post}
        return jsonify(posts[id]), 200
    else:
        return jsonify({"error": "Post not found"}), 404

@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    if id in posts:
        del posts[id]
        return jsonify({"message": "Post deleted"}), 200
    else:
        return jsonify({"error": "Post not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)