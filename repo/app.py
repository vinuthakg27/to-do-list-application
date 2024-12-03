from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up the database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Create a model for the Todo items
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id} - {self.task}>'

# Home route (to display to-do list)
@app.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

# Add new task route
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    new_task = Todo(task=task)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Mark task as done route
@app.route('/done/<int:id>')
def done(id):
    task = Todo.query.get(id)
    task.done = True
    db.session.commit()
    return redirect(url_for('index'))

# Delete task route
@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create the database (only need to run this once)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
