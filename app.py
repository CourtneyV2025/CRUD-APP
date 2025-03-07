from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, timezone 

# Create Flask app instance 
app = Flask(__name__)

# Create SQLite database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

# Define model of a to do list TASK 
class Task(db.Model):
    # db.Column is a column in the database
    # also specify data type of that key 
    # PICK ONE to be the "primary_key"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # String representation of the object 
    def __repr__(self):
        return f'<Task {self.id}>'

# Flask route for displaying all tasks 
@app.route('/', methods=['GET', 'POST'])
def index(): 
    # ADD new Task to database
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    # SELECT all task objects from database
    tasks = Task.query.order_by()
    return render_template('index.html', tasks=tasks)

# Create the database inastance in main method 
if __name__ == "__main__": 
    with app.app_context():
        db.create_all() 
    app.run(host="0.0.0.0", port=5421, debug=True)