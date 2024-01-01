from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import request
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

secret_key = os.getenv('SECRET_KEY')

# App instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{secret_key}@localhost:3306/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# Database initialization
db = SQLAlchemy(app)

# Model definition with default values
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize the database
def initialize_database():
    with app.app_context():
        db.create_all()

# Route for testing
@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "Hello World"
    })

# Create a new item to the database
@app.route("/api/todo", methods=['POST'] )
def post_form_data():
    data = request.get_json()
    todo_item = data.get('todo_item')
    status = data.get('status')
    new_todo = Todo(todo_item=todo_item, status=status)
    db.session.add(new_todo)
    db.session.commit()
    return 'Done', 201

# Read a new item from the database
@app.route("/api/all_todo", methods=['GET'] )
def get_todo_data():
    todos = Todo.query.all()
    # Convert todos to a list of dictionaries
    todos_list = [{'id': todo.id,'todo_item': todo.todo_item, 'status': todo.status} for todo in todos]
    return jsonify(todos_list)

# Update a specific resource
@app.route("/api/update_specific_todo/<int:id>", methods=['PUT'])
def update_specific_todo_data(id):
    data = request.get_json()
    todo_to_update = Todo.query.get(id)
    new_todo_item = data.get('todo_item')
    todo_to_update.todo_item = new_todo_item
    db.session.commit()
    return jsonify(todo_to_update)

# Delete resource
@app.route("/api/delete_specific_todo/<int:id>", methods=['DELETE'])
def delete_specific_todo_data(id):
    todo_to_delete = Todo.query.get(id)
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return jsonify({'message': 'Todo was successfully deleted'})
    else:
        return jsonify({'error': 'Todo not found'}), 404



# Run the application
if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, port=8080)
